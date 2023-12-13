#! python
# -*- coding: UTF-8 -*-

import sys
import os
import yaml
import pickle

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

params = yaml.safe_load(open("params.yaml"))["tree"]
bank_params = yaml.safe_load(open("params.yaml"))["general"]

max_depth = params["max_depth"]
n_estimators = params["n_estimators"]
eta = params["eta"]
reg_lambda = params["reg_lambda"]
reg_alpha = params["reg_alpha"]
scale_pos_weight = params["scale_pos_weight"]

bank = bank_params["bank_id"]

train_data = pd.read_csv(sys.argv[1], sep=';')

X_train = train_data.drop('Y', axis=1)
y_train = train_data['Y']

f_output = os.path.join(os.getcwd(), f'models//model_{bank_params["train_method"]}_{bank}.pkl')

#Если балансируем классы, то на выходе ~0,34 accuracy параметр для балансировки class_weight="balanced"
# clf = DecisionTreeClassifier(max_depth=max_depth, max_features="auto", criterion="log_loss", max_leaf_nodes=0.5)
# clf.fit(X_train, y_train)


# Create and train the XGBoost model
model = XGBClassifier(n_estimators=n_estimators,
                      max_depth=max_depth,
                      device='gpu',
                      eta=eta,
                      sampling_method='gradient_based',
                      reg_lambda=reg_lambda,
                      reg_alpha=reg_alpha,
                      scale_pos_weight=scale_pos_weight)
# Fit the model
model.fit(X_train, y_train)

with open(f_output, "wb") as fd:
    pickle.dump(model, fd)