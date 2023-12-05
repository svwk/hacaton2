#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage

import pandas as pd
import numpy as np

def create_features_in_dataset(source_dataset):
    """
    Создание новых признаков и удаление ненужных
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    education = pd.get_dummies(df['education'])
    value = pd.get_dummies(df['Value'])
    employment_status = pd.get_dummies(df['employment status'])
    family_status = pd.get_dummies(df['Family status'])
    loan_term = pd.get_dummies(df['Loan_term'])
    goods_category = pd.get_dummies(df['Goods_category'])
    merch_code = pd.get_dummies(df['Merch_code'])

    df['Credit_load'] = (df['MonthProfit'] - df['MonthExpense']) / (df['Loan_amount'] / df['Loan_term'])
    df['Credit_load'] = np.where(df['Credit_load'] < 0, 0, df['Credit_load'])
    df['is_loanable'] = np.where(df['Credit_load'] > 1.25, 1, 0)

    df = pd.concat(
        [df, value, education, employment_status, family_status, loan_term, goods_category, merch_code],
        axis=1
    )

    return df


create_stage("create_features", create_features_in_dataset)