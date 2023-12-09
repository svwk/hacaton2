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
    df['Goods_category'] = df['Goods_category'].astype('category')
    df['Merch_code'] = df['Merch_code'].astype('category')
    df['Family status'] = df['Family status'].astype('category')
    df['education'] = df['education'].astype('category')
    df['employment status'] = df['employment status'].astype('category')
    df['Value'] = df['Value'].astype('category')

    df['BankA_decision'] = pd.Categorical(df['BankA_decision'], ordered=True)
    df['BankB_decision'] = pd.Categorical(df['BankB_decision'], ordered=True)
    df['BankC_decision'] = pd.Categorical(df['BankC_decision'], ordered=True)
    df['BankD_decision'] = pd.Categorical(df['BankD_decision'], ordered=True)
    df['BankE_decision'] = pd.Categorical(df['BankE_decision'], ordered=True)

    df['BankA_decision'] = df['BankA_decision'].cat.codes
    df['BankB_decision'] = df['BankB_decision'].cat.codes
    df['BankC_decision'] = df['BankC_decision'].cat.codes
    df['BankD_decision'] = df['BankD_decision'].cat.codes
    df['BankE_decision'] = df['BankE_decision'].cat.codes

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

    # df = df.drop(columns=[
    #     'education',
    #     'Value',
    #     'employment status',
    #     'Family status',
    #     'Loan_term',
    #     'Goods_category',
    #     'Merch_code'
    # ])

    df['Goods_category'] = df['Goods_category'].cat.codes
    df['Merch_code'] = df['Merch_code'].cat.codes
    df['Family status'] = df['Family status'].cat.codes
    df['education'] = df['education'].cat.codes
    df['employment status'] = df['employment status'].cat.codes
    df['Value'] = df['Value'].cat.codes

    return df


create_stage("create_features", create_features_in_dataset)