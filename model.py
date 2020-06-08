from queryspec import Intent, QueryParameters
import nltk
import string
from typing import Tuple, List, Iterable
from labeled_data import get_training_data
import re
from catboost import CatBoostClassifier
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from difflib import get_close_matches
from collections import defaultdict
import pickle

"""This is for parsing the intent from a message, as well as extracting the relevant information
from a message based on the intent"""

import warnings

warnings.filterwarnings("ignore", category=UserWarning)


class Model:
    def __init__(self, args, datastore=None, iohandler=None):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.tfidf = TfidfVectorizer(tokenizer=str.split)
        self.model = CatBoostClassifier(silent=True)

        self.train_tfidf()

        if args.new_model or args.init:
            self.new_model()
        else:
            self.load_model()

    def new_model(self):
        self.train_model()
        self.save_model()

    def save_model(self):
        self.model.save_model("saved_model.cbm")

    def load_model(self):
        self.model.load_model("saved_model.cbm")

    def train_model(self):
        """Creates and trains a CatBoost algorithm on the sample query data."""
        labeled_data = get_training_data()

        features = [self.get_features(query) for query in labeled_data.keys()]
        intents = [intent.name for intent in labeled_data.values()]

        self.model.fit(features, intents)

    def train_tfidf(self):
        documents = self.get_compound_strings()

        self.tfidf.fit(documents)

    def clean_strings(self, strings: Iterable[str]) -> List[str]:
        lemmatizer = WordNetLemmatizer()
        punctuation = string.punctuation.replace("[", "").replace("]", "")

        new_strings = []

        for current_string in strings:
            words = (
                current_string.translate(str.maketrans("", "", punctuation))
                .lower()
                .split()
            )

            clean_string = " ".join(lemmatizer.lemmatize(word) for word in words)

            new_strings.append(clean_string)

        return new_strings

    def get_compound_strings(self) -> List[str]:
        use_individual = False  # can be used to see if using the individual examples, instead of compounding them, as the documents is any better

        if use_individual:
            data = get_training_data()
            return self.clean_strings(query for query, intent in data)

        examples = defaultdict(list)

        with open("query.txt") as infile:
            lines = infile.readlines()

        for line in lines:
            components = line.split("|")

            query = components[1]
            intent = components[3]

            examples[intent].append(query)

        strings = [" ".join(queries) for queries in examples.values()]

        return self.clean_strings(strings)

    def get_features(self, query):
        """Extracts the features from a generalized query.
        Uses uneven weighting to ensure that the type of variable matches the predicted intent.
        Ignores stop words and weights the remaining words evenly."""

        clean_query = self.clean_strings([query])[0]

        return self.tfidf.transform([clean_query]).toarray()[0]

    def extract_variables(self, query: str) -> Tuple[str, List[str]]:
        """Takes in a raw query from the user and extracts the variables from the query, then generalizes the query.
            Returns the generalized form of the query and the list of variables."""
        # Remove course prefixes and punctuation
        query = "".join([c for c in query if c not in string.punctuation])
        query = query.replace("STAT", "").replace("course", "class").lower()
        tags = nltk.pos_tag(nltk.word_tokenize(query))
        stop_words = set(nltk.corpus.stopwords.words("english"))
        topic_words = {"on", "about", "covering", "cover", "involve"}
        terms = {"summer", "spring", "fall", "winter"}
        teacher_titles = {
            "professor",
            "prof",
            "prof.",
            "doctor",
            "dr.",
            "dr",
            "mrs.",
            "mrs",
            "mr.",
            "mr",
            "mister",
            "ms.",
            "ms",
            "miss",
            "instructor",
        }

        titles = self.datastore.get_course_titles()
        professor_names = self.datastore.get_professor_names()
        vars = []
        general_query = ""

        i = 0
        found_title = False
        while i < len(tags):
            found_variable = False
            # Check for a professor's name, spelled reasonably closely
            matches = get_close_matches(tags[i][0], professor_names, n=1, cutoff=0.9)
            if len(matches) > 0:
                vars.append(matches[0])
                general_query += "[professor] "
                found_variable = True
            # Use a sliding window to check every subsequence for a possible class title
            if not found_title:
                j = 0
                while j < i:
                    # Only match to a course title if the phrase is very close
                    phrase = " ".join([t[0].capitalize() for t in tags[j : i + 1]])
                    matches = get_close_matches(phrase, titles, n=1, cutoff=0.7)
                    if len(matches) > 0:
                        found_title = True
                        found_variable = True
                        vars.append(matches[0])
                        general_query = general_query.replace(
                            " ".join([t[0] for t in tags[j:i]]), ""
                        )
                        general_query += "[class] "
                        break
                    j += 1
            # Class id found
            if tags[i][1] == "CD" and "[class] " not in general_query:
                vars.append(tags[i][0])
                general_query += "[class] "
                found_variable = True
            # Term name found
            elif tags[i][0].lower() in terms:
                vars.append(tags[i][0].lower())
                general_query += "[term] "
                found_variable = True
            # Professor name found, preceeded by a title
            elif (
                tags[i][0].lower() in teacher_titles
                and "[professor] " not in general_query
                and i < len(tags) - 1
            ):
                vars.append(tags[i + 1][0].lower())
                general_query += "[professor] "
                found_variable = True
                i += 1
            # Connecting word that introduces a topic found
            elif tags[i][0] in topic_words and i < len(tags) - 1:
                j = i + 1
                topic = ""
                # Get the entire topic
                while j < len(tags):
                    if tags[j][0] in stop_words:
                        break
                    topic += " " + tags[j][0].lower()
                    j += 1
                general_query += tags[i][0] + " "
                general_query += "[topic] "
                vars.append(topic.strip())
                i = j - 1
                found_variable = True

            if not found_variable:
                general_query += tags[i][0]
                general_query += " "
            i += 1
        return re.sub(" +", " ", general_query.strip()), vars

    def get_intent_and_params(self, message: str) -> Tuple[Intent, QueryParameters]:
        """Takes in a raw message, and determines its intent and parameters, returning Intent.UNKNOWN 
        if it can not determine within some tolerance. It is permitted,
        and encouraged, to ask additional questions to determine a users intent"""
        generalized, variables = self.extract_variables(message)
        params = self.create_query_params(generalized, variables)
        vector = self.get_features(generalized)

        prediction = self.model.predict(vector)[0]

        return Intent[prediction], params

    def create_query_params(
        self, generalized: str, variables: List[str]
    ) -> QueryParameters:
        """Creates a QueryParameters object from a generalized query and its variables."""
        var_locations = re.findall(r"(\[(.*?)\])", generalized)
        class_id = None
        term = None
        professor = None
        topic = None
        for i in range(len(var_locations)):
            if var_locations[i][0] == "[class]":
                if variables[i].isdigit():
                    class_id = int(variables[i])
                else:
                    class_id = self.datastore.get_id_of_class(variables[i])
            elif var_locations[i][0] == "[term]":
                term = variables[i]
            if var_locations[i][0] == "[professor]":
                professor = variables[i]
            if var_locations[i][0] == "[topic]":
                topic = variables[i]
        return QueryParameters(class_id, term, professor, topic)
