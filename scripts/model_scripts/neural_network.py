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
from model_methods import clear_train_test_data_frame


params = yaml.safe_load(open("params.yaml"))["neural"]
bank_params = yaml.safe_load(open("params.yaml"))["bank"]

max_depth = params["max_depth"]
learning_rate = params["learning_rate_init"]
verbose = params["verbose"]
hidden_layer_x = params["hidden_layer_sizes_x"]
hidden_layer_y = params["hidden_layer_sizes_y"]

bank = bank_params["bank_id"]

train_data = pd.read_csv(sys.argv[1], sep=';')

X_train = clear_train_test_data_frame(train_data, bank)
y_train = train_data[f'решение банка {bank}']

#Так как данные не сбалансированы, применяем метод балансировки
nm = NearMiss()
X_train_miss, Y_train_miss = nm.fit_resample(X_train, y_train)

f_output = os.path.join(os.getcwd(), f'models//model_net_{bank}.pkl')

neural_net = MLPClassifier(hidden_layer_sizes=(hidden_layer_x, hidden_layer_y),
                    verbose=verbose,
                    max_iter = max_depth,
                    learning_rate_init=learning_rate)

neural_net.fit(X_train_miss, Y_train_miss)

with open(f_output, "wb") as fd:
    pickle.dump(neural_net, fd)