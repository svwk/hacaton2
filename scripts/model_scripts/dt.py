#! python
# -*- coding: UTF-8 -*-

import sys
import os
import yaml
import pickle

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

train_data = pd.read_csv(sys.argv[1], sep=';')

print(train_data.head(1))

X_train = train_data.drop(f'решение банка {sys.argv[3]}', axis=1)
X_train = X_train.drop('образование', axis=1)
X_train = X_train.drop('тип занятости', axis=1)
X_train = X_train.drop('стаж работы', axis=1)
X_train = X_train.drop('семейное положение', axis=1)
X_train = X_train.drop('категория товара', axis=1)
X_train = X_train.drop('стаж работы на последнем месте', axis=1)
y_train = train_data[f'решение банка {sys.argv[3]}']

params = yaml.safe_load(open("params.yaml"))["tree"]

f_output = os.path.join(os.getcwd(), f"models//{sys.argv[2]}")

max_depth = params["max_depth"]
seed = params["seed"]

clf = DecisionTreeClassifier(max_depth=max_depth, random_state=seed)
clf.fit(X_train, y_train)

with open(f_output, "wb") as fd:
    pickle.dump(clf, fd)