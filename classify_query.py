from random import choice, sample
import numpy as np
import nltk
import string
import csv
from sys import argv
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import metrics
from collections import defaultdict
from typing import Tuple, List
from model import Model
from main import get_args
from datastore import DataStore
import random
from sklearn.metrics import classification_report


"""This file is an experimental file for ML classification and query parsing. It is not intended to be used as production code."""


class Record:
    def __init__(self, query, answer):
        self.query = query
        self.answer = answer

    def __repr__(self):
        return str(self.query) + " | " + str(self.answer)


# Only use intents that have at least two records
def get_records(records):
    classes = {}
    new_records = []
    for record in records:
        classes[record.answer] = 1
        new_records.append(record)

    for cid in classes:
        records_of_intent = [v for v in records if v.answer == cid]
        if len(records_of_intent) < 2:
            for record in records_of_intent:
                new_records.remove(record)
    return new_records


def main():
    records = []
    variables = []
    test = []
    corpus = {}
    stop_words = set(nltk.corpus.stopwords.words("english"))
    # nltk.download("averaged_perceptron_tagger")
    # nltk.download("tagsets")
    # nltk.download("punkt")
    punc = r"""!()-{};:'"\,<>./?@#$%^&*_~"""
    with open("query.txt") as fd:
        lines = fd.readlines()
        #print(lines)
        lines = [x.strip().translate(str.maketrans("", "", punc)) for x in lines]
        #print(lines)
        items = [x.split("|") for x in lines]
        items = [i for i in items if i[0] == "B4"]
        for item in items:
            words = item[1].split(" ")
            records.append(Record(item[1], item[2]))
        #print(records)

    validate(records)

    args = get_args()
    datastore = DataStore(args)
    model = Model(args, datastore, None)
    model.train_model(records)

    with open("test_queries.txt") as fd:
        lines = fd.readlines()
        lines = [x.strip().translate(str.maketrans("", "", punc)) for x in lines]
        queries = [x.replace("STAT", "") for x in lines]

        for query in queries:
            test.append(model.extract_variables(query))

    #print(test)

    for query in test:
        #print(query[0] + ": " + model.predict_query(query[0]))
        # + " | " + str(query[1]))
        pass

    # # Test-train split, 80% train 20% test
    #records = get_records(records)


def assist_validation(my_data, model, test):
    features = [model.get_features(r.query) for r in my_data]
    #print(features)
    vectors = []
    # Get a corpus of every feature in the training set
    if test == False:
        for extracted in features:
            for feature in extracted:
                if feature not in model.feature_vector:
                    model.feature_vector[feature] = 0
    #print(model.feature_vector)

    #print(self.feature_vector)
    #print(features)
    # Create a feature vector from the entire corpus for each training record
    for vector in features:
        new_features = dict.fromkeys(model.feature_vector, 0)
        for feature in vector.keys():
            #print(new_features.keys())
            if feature in new_features.keys():
                #print(feature)
                new_features[feature] = vector[feature]
        # Convert to values only
        new_features = np.array(list(new_features.values()))
        vectors.append(new_features)
    return vectors

    
def validate(records):
    # X_train, X_test, y_train, y_test = train_test_split(
    #     [r.query for r in records],
    #     [r.answer for r in records],
    #     train_size=0.7
    # )
    random.shuffle(records)
    split = len(records) // 4
    # print(records)
    test = records[:split]
    train = records[split:]

    X_train = []
    y_train = []

    X_test = []
    y_test = []

    args = get_args()
    datastore = DataStore(args)
    model = Model(args, datastore, None)

    X_train = assist_validation(train, model, False)
    X_test = assist_validation(test, model, True)

    for trainrecord in train:
        y_train.append(trainrecord.answer)

    for testrecord in test:
        y_test.append(testrecord.answer)

            #stratify=[r.answer for r in records]

    model = KNeighborsClassifier(n_neighbors = 1)

    model.fit(X_train, y_train)



    # print(len(X_test))
    # print(len(y_test))

    # X_test = [item.reshape(1,-1) for item in X_test1]

    y_pred = model.predict(X_test)

    # print(y_pred)
    # print(y_test)

    print(classification_report(y_test, y_pred))

    # print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    # print(
    #     "Average Precision:",
    #     metrics.precision_score(y_test, y_pred, average="weighted"),
    # )
    # print("Average Recall:", metrics.recall_score(y_test, y_pred, average="weighted"))
    # print("Average F1:", metrics.f1_score(y_test, y_pred, average="weighted"))


if __name__ == "__main__":
    main()
