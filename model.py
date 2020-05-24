from queryspec import Intent
import nltk
import string
import re
from sklearn.neighbors import KNeighborsClassifier
from nltk.stem import WordNetLemmatizer
from typing import Tuple, List
import numpy as np


"""This is for parsing the intent from a message, as well as extracting the relevant information
from a message based on the intent"""


class Model:
    def __init__(self, args, datastore, iohandler):
        self.args = args
        self.datastore = datastore
        self.iohandler = iohandler
        self.model = None
        nltk.download("wordnet")
        self.feature_vector = {}

        # -> Tuple[str, typing.List[str]]:

    def extract_variables(self, query: str) -> Tuple[str, List[str]]:
        """Takes in a raw query from the user and extracts the variables from that query, then generalizes the query.
            Returns the list of variables and the generalized form of that query."""
        tokens = nltk.word_tokenize(query)
        tags = nltk.pos_tag(tokens)
        general_query = ""
        terms = ["summer", "spring", "fall", "winter"]
        vars = []
        stop_words = set(nltk.corpus.stopwords.words("english"))
        topic_words = ["on", "about", "covering"]
        i = 0
        while i < len(tags):
            # Class id found
            if tags[i][1] == "CD":
                vars.append(tags[i][0])
                general_query += "[CLASS] "
                # A list of classes is represented as [CLASSES]
                # if "[CLASS]" in general_query:
                #     general_query = general_query.replace("[CLASS]", "[CLASSES]")
                # elif "[CLASSES]" not in general_query:
                #     general_query += "[CLASS] "
            # Term name found
            elif tags[i][0].lower() in terms:
                vars.append(tags[i][0].lower())
                general_query += "[TERM] "  # why no space here?
            # Connecting word that introduces a topic found
            elif tags[i][0] in topic_words:
                j = i + 1
                # Get the entire topic
                while j < len(tags):
                    if (
                        tags[j][0] in stop_words
                    ):  # you think that this means the intent is finished?
                        break
                    vars.append(tags[j][0].lower())
                    j += 1
                general_query += tags[i][0] + " "
                general_query += "[TOPIC] "
                i = j - 1
            else:
                general_query += tags[i][0]
                general_query += " "
            i += 1
        return general_query.strip(), vars

    def train_model(self, training):
        """Creates and trains a K-nearest-neighbors algorithm on the query data."""
        model = KNeighborsClassifier(n_neighbors=1)
        # Extract features from test set
        features = [self.get_features(r.query) for r in training]
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
        model.fit(vectors, [r.answer for r in training])
        self.model = model

    def predict_query(self, query):
        """Predicts the answer type of a generalized query."""
        vector = self.get_features(query)
        features = dict.fromkeys(self.feature_vector, 0)
        # Create a feature vector from the entire corpus
        for feature in vector.keys():
            # Inore any features not in training set
            if feature in features:
                features[feature] = vector[feature]
        features = np.array(list(features.values()))
        return self.model.predict([features])[0]

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
            features[var[0]] = 100
            query = query.replace(var[0], "")

        # Tokenize, lowercase, and lemmatize all non-variable words, then remove all stop words
        words = nltk.word_tokenize(query)
        words = [word.lower() for word in words]
        words = [wordnet_lemmatizer.lemmatize(w) for w in words]
        words = [w for w in words if w not in stop_words]

        # Add all non-stop words to features with weight of 50
        for word in words:
            features[word] = 50
        return features

    def get_intent(self, message: str) -> Intent:
        """Takes in a raw message, and determines its intent, returning Intent.UNKNOWN
        if it can not determine within some tolerance. It is permitted, and encouraged, to ask 
        additional questions to determine a users intent"""
        return Intent.UNKNOWN

    def get_course_id(self, message: str) -> int:
        """This method is very important, being called on all but one intents. 
        It takes in a raw message, and determines which single course it is refering to.
        It could be in the form of some or parts of its title, or its course id.
        It should aggressively try its options to come up with its best guess, or None if it has no idea"""
        return 312
