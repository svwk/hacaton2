#! python
# -*- coding: UTF-8 -*-

import os
import sys
import pickle
import json
import yaml

import pandas as pd
from sklearn.metrics import accuracy_score, cohen_kappa_score, hamming_loss
from sklearn.metrics import classification_report, f1_score
from model_methods import clear_train_test_data_frame


if len(sys.argv) != 4:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython evaluate.py data-file model\n")
    sys.exit(1)

test_data = pd.read_csv(sys.argv[1], sep=';')

bank_params = yaml.safe_load(open("params.yaml"))["bank"]

x_test = clear_train_test_data_frame(test_data, bank_params["bank_id"])
y_test = test_data[f'решение банка {bank_params["bank_id"]}']

with open(sys.argv[2], "rb") as fd:
    clf = pickle.load(fd)

score = clf.score(x_test, y_test)

preds = clf.predict(x_test)

prc_file = os.path.join("evaluate", sys.argv[3])
os.makedirs(os.path.join("evaluate"), exist_ok=True)

f1 = classification_report(y_test, preds, target_names=['negative', 'meaning', 'positive'], zero_division=True)
print(f1)

f1_micro = f1_score(y_test, preds, average="micro")

with open(prc_file, "w") as fd:
    json.dump({"micro_f1": f1_micro}, fd)
