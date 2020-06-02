from queryspec import Intent, QueryParameters
import nltk
import string
from typing import Tuple, List
from labeled_data import get_training_data
import re
from catboost import CatBoostClassifier
from nltk.stem import WordNetLemmatizer
from typing import Tuple, List
from difflib import get_close_matches
import numpy as np


"""This is for parsing the intent from a message, as well as extracting the relevant information
from a message based on the intent"""


class Model:
    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.model = None
        self.feature_vector = {}

    def train_model(self):
        """Creates and trains a CatBoost algorithm on the sample query data."""
        model = CatBoostClassifier(silent=True)
        # Extract features from test set
        query_intent_map = get_training_data()
        training = query_intent_map.keys()
        features = [self.get_features(r) for r in training]
        intents = [query_intent_map[r].name for r in training]
        vectors = []
        # Get a corpus of every feature in the training set
        for extracted in features:
            for feature in extracted:
                if feature not in self.feature_vector:
                    self.feature_vector[feature] = 0

        # Create a feature vector from the entire corpus for each training record
        for vector in features:
            new_features = dict.fromkeys(self.feature_vector, 0)
            for feature in vector.keys():
                new_features[feature] = vector[feature]
            # Convert to values only
            new_features = np.array(list(new_features.values()))
            vectors.append(new_features)
        model.fit(vectors, intents)
        self.model = model

    def get_features(self, query):
        """Extracts the features from a generalized query.
        Uses uneven weighting to ensure that the type of variable matches the predicted intent.
        Ignores stop words and weights the remaining words evenly."""
        features = {}
        stop_words = set(nltk.corpus.stopwords.words("english"))
        wordnet_lemmatizer = WordNetLemmatizer()
        # First get all the variables out and weight them twice as much as everything else, weight of 100
        variables = re.findall(r"(\[(.*?)\])", query)
        for var in variables:
            features[var[0]] = 3
            query = query.replace(var[0], "")

        # Tokenize, lowercase, and lemmatize all non-variable words
        query = "".join([c for c in query if c not in string.punctuation])
        words = nltk.word_tokenize(query)
        words = [word.lower() for word in words]
        words = [word for word in words if word not in string.punctuation]
        words = [wordnet_lemmatizer.lemmatize(w) for w in words]

        # Add first word to features with weight of 50, changes intent drastically.
        features[words[0]] = 2
        for word in words[1:]:
            # Add all non-stop words to features with weight of 15
            # if word not in stop_words:
            features[word] = 1
        return features

    def extract_variables(self, query: str) -> Tuple[str, List[str]]:
        """Takes in a raw query from the user and extracts the variables from the query, then generalizes the query.
            Returns the generalized form of the query and the list of variables."""
        query = "".join([c for c in query if c not in string.punctuation])
        tags = nltk.pos_tag(nltk.word_tokenize(query))
        stop_words = set(nltk.corpus.stopwords.words("english"))
        topic_words = ["on", "about", "covering", "cover"]
        terms = ["summer", "spring", "fall", "winter"]
        teacher_titles = ["professor", "prof", "mr", "mrs"]
        titles = self.datastore.get_course_titles()
        professor_names = self.datastore.get_professor_names()
        # Remove course prefixes, if any
        query = query.replace("STAT", "")
        vars = []
        general_query = ""

        i = 0
        found_title = False
        while i < len(tags):
            found_variable = False
            # Check for a professor's name, spelled reasonably closely
            matches = get_close_matches(tags[i][0], professor_names, n=1, cutoff=0.8)
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
                    matches = get_close_matches(phrase, titles, n=1, cutoff=0.9)
                    if len(matches) > 0:
                        found_title = True
                        found_variable = True
                        vars.append(matches[0])
                        general_query = general_query.replace(
                            " ".join([t[0] for t in tags[j:i]]), ""
                        )
                        general_query += "[class] "
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
        features = dict.fromkeys(self.feature_vector, 0)
        # Create a feature vector from the entire corpus
        for feature in vector.keys():
            # Inore any features not in training set
            if feature in features:
                features[feature] = vector[feature]
        features = np.array(list(features.values()))
        return Intent[self.model.predict(features)[0]], params

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
