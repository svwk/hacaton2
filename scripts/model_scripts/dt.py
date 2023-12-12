#! python
# -*- coding: UTF-8 -*-

import sys
import os
import yaml
import pickle

import pandas as pd

from model_methods import clear_train_test_data_frame
from sklearn.tree import DecisionTreeClassifier

params = yaml.safe_load(open("params.yaml"))["tree"]
bank_params = yaml.safe_load(open("params.yaml"))["bank"]

max_depth = params["max_depth"]
bank = bank_params["bank_id"]

train_data = pd.read_csv(sys.argv[1], sep=';')

X_train = clear_train_test_data_frame(train_data, bank)
y_train = train_data[f'решение банка {bank}']

f_output = os.path.join(os.getcwd(), f'models//model_tree_{bank}.pkl')

#Если балансируем классы, то на выходе ~0,34 accuracy параметр для балансировки class_weight="balanced"
clf = DecisionTreeClassifier(max_depth=max_depth, max_features="auto", criterion="log_loss")
clf.fit(X_train, y_train)

with open(f_output, "wb") as fd:
    pickle.dump(clf, fd)