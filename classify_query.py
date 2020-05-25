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


"""This file is an experimental file for ML classification and query parsing. It is not intended to be used as production code."""


class Record:
    def __init__(self, query, answer):
        self.query = query
        self.answer = answer


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
    nltk.download("averaged_perceptron_tagger")
    nltk.download("tagsets")
    nltk.download("punkt")
    punc = r"""!()-{};:'"\,<>./?@#$%^&*_~"""
    with open("data.txt") as fd:
        lines = fd.readlines()
        lines = [x.strip().translate(str.maketrans("", "", punc)) for x in lines]
        items = [x.split("|") for x in lines]

        for item in items:
            words = item[1].split(" ")
            records.append(Record(item[1], item[2]))

    model = Model(None, None, None)
    model.train_model(records)

    with open("queries.txt") as fd:
        lines = fd.readlines()
        lines = [x.strip().translate(str.maketrans("", "", punc)) for x in lines]
        queries = [x.replace("STAT", "") for x in lines]

        for query in queries:
            test.append(model.extract_variables(query)[0])

    for query in test:
        print(query + ": " + model.predict_query(query))

    # # # Test-train split, 80% train 20% test
    # records = get_records(records)
    # X_train, X_test, y_train, y_test = train_test_split(
    #     [r.query for r in records],
    #     [r.answer for r in records],
    #     train_size=0.6,
    #     stratify=[r.answer for r in records],
    # )

    # print(y_train)
    # print(y_test)
    # # Use TF-IDF for features
    # tfid = TfidfVectorizer(stop_words=stop_words)
    # tfid.fit([r.query for r in records])
    # X_train = tfid.transform(X_train)
    # X_test = tfid.transform(X_test)

    # model = KNeighborsClassifier(n_neighbors=4)

    # model.fit(X_train, y_train)

    # y_pred = model.predict(X_test)

    # print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    # print(
    #     "Average Precision:",
    #     metrics.precision_score(y_test, y_pred, average="weighted"),
    # )
    # print("Average Recall:", metrics.recall_score(y_test, y_pred, average="weighted"))
    # print("Average F1:", metrics.f1_score(y_test, y_pred, average="weighted"))


if __name__ == "__main__":
    main()
