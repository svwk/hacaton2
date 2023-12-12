#! python
# -*- coding: UTF-8 -*-

import os
import sys
import pickle
import json
import yaml

import pandas as pd
from sklearn.linear_model import LogisticRegression
from model_methods import clear_train_test_data_frame


params = yaml.safe_load(open("params.yaml"))["log_reg"]
bank_params = yaml.safe_load(open("params.yaml"))["bank"]

max_depth = params["max_depth"]
treshold = params["treshold"]
bank = bank_params["bank_id"]

train_data = pd.read_csv(sys.argv[1], sep=';')

print(train_data.head(1))

X_train = clear_train_test_data_frame(train_data, bank)
y_train = train_data[f'решение банка {bank}']

f_output = os.path.join(os.getcwd(), f'models//model_log_{bank}.pkl')

log_reg = LogisticRegression(max_iter=max_depth)
log_reg.fit(X_train, y_train)

with open(f_output, "wb") as fd:
    pickle.dump(log_reg, fd)