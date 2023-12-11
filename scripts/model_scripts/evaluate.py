#! python
# -*- coding: UTF-8 -*-

import os
import sys
import pickle
import json

import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, hamming_loss

if len(sys.argv) != 5:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython evaluate.py data-file model\n")
    sys.exit(1)

test_data = pd.read_csv(sys.argv[1], sep=';')

print(test_data.head(2))

x_test = test_data.drop(f'решение банка {sys.argv[4]}', axis=1)
x_test = x_test.drop('образование', axis=1)
x_test = x_test.drop('тип занятости', axis=1)
x_test = x_test.drop('стаж работы', axis=1)
x_test = x_test.drop('семейное положение', axis=1)
x_test = x_test.drop('категория товара', axis=1)
x_test = x_test.drop('стаж работы на последнем месте', axis=1)
y_test = test_data[f'решение банка {sys.argv[4]}']

with open(sys.argv[2], "rb") as fd:
    clf = pickle.load(fd)

score = clf.score(x_test, y_test)

preds = clf.predict(x_test)

a = accuracy_score(y_test, preds)
c = cohen_kappa_score(y_test, preds)
h = hamming_loss(y_test, preds)

prc_file = os.path.join("evaluate", sys.argv[3])
os.makedirs(os.path.join("evaluate"), exist_ok=True)

with open(prc_file, "w") as fd:
    json.dump({"score": score, "accuracy": a, "c": c, "error": h}, fd)
