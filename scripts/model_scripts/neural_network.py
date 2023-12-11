#! python
# -*- coding: UTF-8 -*-

import sys
import os
import yaml
import pickle

import pandas as pd
import numpy as np

from sklearn.neural_network import MLPClassifier
from imblearn.under_sampling import NearMiss


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

#Так как данные не сбалансированы, применяем метод балансировки
nm = NearMiss()
X_train_miss, Y_train_miss = nm.fit_resample(X_train, y_train)

params = yaml.safe_load(open("params.yaml"))["neural"]

f_output = os.path.join(os.getcwd(), f"models//{sys.argv[2]}")

max_depth = params["max_depth"]
seed = params["seed"]

neural_net = MLPClassifier(hidden_layer_sizes=(6,2),
                    random_state=seed,
                    verbose=True,
                    max_iter = max_depth,
                    learning_rate_init=0.01)

neural_net.fit(X_train_miss, Y_train_miss)

with open(f_output, "wb") as fd:
    pickle.dump(neural_net, fd)