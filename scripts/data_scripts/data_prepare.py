#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage

import pandas as pd
import numpy as np

def prepare_dataset(source_dataset):
    """
    Начальная подготовка датасета
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    df['SkillFactory_Id'] = df['SkillFactory_Id'].astype('int')
    df['BirthDate'] = pd.to_datetime(df['BirthDate'])
    df['education'] = df['education'].astype('category')
    df['employment status'] = df['employment status'].astype('category')
    df['Value'] = df['Value'].astype('category')
    df['JobStartDate'] = pd.to_datetime(df['JobStartDate'])
    df['Gender'] = np.where(df['Gender'] > 0, 1, 0)
    df['Family status'] = df['Family status'].astype('category')
    df['ChildCount'] = df['ChildCount'].fillna(0).astype('int')
    df['SNILS'] = df['SNILS'].fillna(0).astype('int')
    df['Goods_category'] = df['Goods_category'].astype('category')
    df['Merch_code'] = df['Merch_code'].astype('category')

    return df


create_stage("data_prepare", prepare_dataset)
