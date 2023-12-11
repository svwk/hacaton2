#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage

import pandas as pd
import numpy as np
from data_prepare import prepare_dataset
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.seniority_cats import set_last_seniority_cat


def create_features_in_dataset(source_dataset):
    """
    Создание новых признаков и удаление ненужных
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    df = prepare_dataset(df)
    df['is_working'] = ((pd.notna(df['JobStartDate'])) & (df['employment status'] != "Не работаю"))
    df['is_working'] = df['is_working'].astype('int')

    df['Goods_category'] = pd.Categorical(df['Goods_category'], ordered=True)
    df['Merch_code'] = pd.Categorical(df['Merch_code'], ordered=True)
    df['Family status'] = pd.Categorical(df['Family status'], ordered=True)
    df['education'] = pd.Categorical(df['education'], ordered=True)
    df['employment status'] = pd.Categorical(df['employment status'], ordered=True)
    df['Value'] = pd.Categorical(df['Value'], ordered=True)

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

    education = pd.get_dummies(df['education'], prefix="образование", dtype=int)
    value = pd.get_dummies(df['Value'], prefix="общий стаж", dtype=int)
    employment_status = pd.get_dummies(df['employment status'], prefix="занятость", dtype=int)
    family_status = pd.get_dummies(df['Family status'], prefix="cемейное положение", dtype=int)

    loan_term = pd.get_dummies(df['Loan_term'], prefix="cрок кредита", dtype=int)
    goods_category = pd.get_dummies(df['Goods_category'], prefix="kатегория товара", dtype=int)
    merch_code = pd.get_dummies(df['Merch_code'], prefix="код магазина", dtype=int)

    df['кредитная нагрузка'] = (df['MonthProfit'] - df['MonthExpense']) / (df['Loan_amount'] / df['Loan_term'])
    # df['кредитная нагрузка'] = np.where(df['кредитная нагрузка'] < 0, 0, df['кредитная нагрузка'])
    df['кредит возможен'] = np.where(df['кредитная нагрузка'] > 1.25, 1, 0)

    df['возраст'] = df['BirthDate'].apply(lambda r: relativedelta(datetime.today(), r).years)

    # Стаж работы на последнем месте в месяцах

    last_seniority = df.apply(set_last_seniority_cat, axis=1)
    df['стаж работы на последнем месте'] = pd.Categorical(last_seniority, ordered=True)
    last_seniority=pd.get_dummies(df['стаж работы на последнем месте'], prefix="последний стаж", dtype=int)

    df = pd.concat(
        [df, value, education, employment_status, family_status, loan_term, goods_category, merch_code, last_seniority],
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


    df['Loan_term'] = pd.Categorical(df['Loan_term'], ordered=True)

    df = df.drop(columns=['SkillFactory_Id', 'Position', 'BirthDate', 'JobStartDate'])

    df['срок кредита код'] = df['Loan_term'].cat.codes
    df['категория товара код'] = df['Goods_category'].cat.codes
    df['код магазина код'] = df['Merch_code'].cat.codes
    df['семейное положение код'] = df['Family status'].cat.codes
    df['образование код'] = df['education'].cat.codes
    df['тип занятости код'] = df['employment status'].cat.codes
    df['стаж работы код'] = df['Value'].cat.codes
    df['последний стаж код'] = df['Value'].cat.codes

    df = df.rename(columns={
        'MonthProfit': 'ежемесячный доход',
        'MonthExpense': 'ежемесячный расход',
        'Gender': 'пол',
        'SNILS': 'СНИЛС',
        'ChildCount': 'кол-во детей',
        'Goods_category': 'категория товара',
        'Merch_code': 'код магазина',
        'Family status': 'семейное положение',
        'education': 'образование',
        'employment status': 'тип занятости',
        'Value': 'стаж работы',
        'Loan_term': 'срок кредита',
        'Loan_amount': 'сумма заказа',
        'is_working': 'имеет доход',
        'BankA_decision': 'решение банка A',
        'BankB_decision': 'решение банка B',
        'BankC_decision': 'решение банка C',
        'BankD_decision': 'решение банка D',
        'BankE_decision': 'решение банка E',
    })

    return df


if __name__ == "__main__":
    create_stage("create_features", create_features_in_dataset)
