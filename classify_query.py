from random import choice, sample
import numpy as np
import nltk
import string
import csv
from sys import argv
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
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
from sklearn.svm import SVC
from queryspec import Intent
import re
from catboost import CatBoostClassifier
import pandas as pd


"""This file is an experimental file for ML classification and query parsing. It is not intended to be used as production code."""


class Record:
    def __init__(self, query, intent):
        self.query = query
        self.intent = intent

    def __repr__(self):
        return str(self.query) + " | " + str(self.intent)


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

def manip_queries():
    records = []
    with open("merged_queries.txt", "w") as outfile:
        with open("query.txt") as infile:
            lines = infile.readlines()
            items = [x.split("|") for x in lines]
            #items[0][3] = re.sub(r'\n', "", items[0][3]).rstrip()
            #current = items[0][3]
            for i in range(len(items) - 1):
                items[i][1] = re.sub(r"[\.\?]", "", items[i][1])
                items[i][2] = re.sub(r"[\.\?]", "", items[i][2])
                #items[i][3] = re.sub(r'\n', "", items[i][3]).rstrip()
                current = items[i][3]
                if items[i+1][3] == current:
                    outfile.write(str(items[i][1]) + " ")
                else:
                    outfile.write(str(items[i][1]) + " ")
                    outfile.write("|" + str(items[i][3]))
                



def main():
    records = []
    variables = []
    test = []
    corpus = {}
    stop_words = set(nltk.corpus.stopwords.words("english"))
    # nltk.download("averaged_perceptron_tagger")
    # nltk.download("tagsets")
    # nltk.download("punkt")
    #punc = r"""!()-{};:'"\,<>./?@#$%^&*_~"""
    manip_queries()
    documents = []
    records = []
    with open("merged_queries.txt") as fd:
        lines = fd.readlines()
        #print(lines)
        #lines = [x.strip().translate(str.maketrans("", "", punc)) for x in lines]
        #print(lines)
        items = [x.split("|") for x in lines]
        for item in items:
            documents.append(item[0])
        #items = [i for i in items if i[0] == "B4"]
    with open("query.txt") as f:
        lines = f.readlines()
        items = [x.split("|") for x in lines]
        for item in items:
            words = item[1].split(" ")
            item[1] = re.sub(r"[\.\?]", "", item[1])
            #item[2] = re.sub(r"[\.\?]", "", item[2])
            item[3] = re.sub(r'\n', "", item[3]).rstrip()
            #print(item[2])
            records.append(Record(item[1], Intent[item[3]]))
    #print(records)
        #print(records)
    #print(documents)

    tfidf = TfidfVectorizer(stop_words = stop_words)
    tfidf.fit(documents)

    validate(records, tfidf)
    # args = get_args()
    # datastore = DataStore(args)
    # model = Model(args, datastore, None)
    # model.train_model(records)

    # with open("test_queries.txt") as fd:
    #     lines = fd.readlines()
    #     lines = [x.strip().translate(str.maketrans("", "", punc)) for x in lines]
    #     queries = [x.replace("STAT", "") for x in lines]

    #     for query in queries:
    #         test.append(model.extract_variables(query))

    # #print(test)

    # for query in test:
    #     #print(query[0] + ": " + model.predict_query(query[0]))
    #     # + " | " + str(query[1]))
    #     pass

    # # Test-train split, 80% train 20% test
    #records = get_records(records)


def assist_validation(my_data, model, test):
    feature_vectors = [model.get_features(r.query) for r in my_data]
    #print(features)
    #vectors = []
    # Get a corpus of every feature in the training set
    # if test == False:
    #     for extracted in features:
    #         for feature in extracted:
    #             if feature not in model.feature_vector:
    #                 model.feature_vector[feature] = 0
    # #print(model.feature_vector)

    # #print(self.feature_vector)
    # #print(features)
    # # Create a feature vector from the entire corpus for each training record
    # for vector in features:
    #     new_features = dict.fromkeys(model.feature_vector, 0)
    #     for feature in vector.keys():
    #         #print(new_features.keys())
    #         if feature in new_features.keys():
    #             #print(feature)
    #             new_features[feature] = vector[feature]
    #     # Convert to values only
    #     new_features = np.array(list(new_features.values()))
    #     vectors.append(new_features)
    return feature_vectors


# def split_groups(records, test):
#     class_counts = []
#     current_intent = records[0].intent
#     current_count = 0
#     for record in records:
#         if record.intent == current_intent:
#             current_count += 1
#         else:
#             current_intent = record.intent
#             class_counts.append(current_count)
#             current_count = 0
#     class_counts[len(class_counts)-1] += 1
#     random_nums = []
#     for i in range(len(class_counts)):
#         random_nums.append((random.sample(range(class_counts[i]), test), class_counts[i]))
#     return random_nums

    
def validate(records, tfidf):

    args = get_args()
    datastore = DataStore(args)
    model = Model(args, datastore, None)
    data = tfidf.transform([r.query for r in records])
    X_train, X_test, y_train, y_test = train_test_split(
        data,
        [str(r.intent) for r in records],
        train_size=0.8,
        stratify = [str(r.intent) for r in records]
    )
    # random.shuffle(records)
    # split = len(records) // 4
    # print(records)
    # test = records[:split]
    # train = records[split:]


    # class_counts = []
    # train = []
    # test = []

    # print(X_train)
    # print(X_test)

    # my_splits = split_groups(records, 2)

    # for record in records:
    #     current = 0
    #     for i in range(len(my_splits)):

    # for i in range(len(records)):
    #     current_count = 0
    #     if 



    # print(my_splits)

    
    # X_train = []
    # y_train = []

    # X_test = []
    # y_test = []

    # args = get_args()
    # datastore = DataStore(args)
    # model = Model(args, datastore, None)

    # X_train = assist_validation(train, model, False)
    # X_test = assist_validation(test, model, True)

    # for trainrecord in train:
    #     y_train.append(str(trainrecord.intent))

    # for testrecord in test:
    #     y_test.append(str(testrecord.intent))

    #         #stratify=[r.answer for r in records]

    # #model = KNeighborsClassifier(n_neighbors = 1)
    # #model = DecisionTreeClassifier()
    # # model = SVC()
    model = CatBoostClassifier()

    model.fit(X_train, y_train)



    # print(len(X_test))
    # print(len(y_test))

    # X_test = [item.reshape(1,-1) for item in X_test1]

    y_pred = model.predict(X_test)

    misclassified = np.where(y_test != y_pred)


    y_pred1 = [obs[0] for obs in y_pred]
    y_test1 = [obs[0] for obs in y_test]
    # print(y_pred1)
    # print(y_test)
    frame = pd.DataFrame(y_test, y_pred)
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also

    #     print(frame)

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
