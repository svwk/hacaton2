#! python
# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
from data_prepare import prepare_dataset

from data_methods import create_stage

def feature_prepare_in_dataset(source_dataset):
    """
    Создание новых признаков и удаление ненужных
    :param source_dataset:  Исходный датасет
    """
    df = source_dataset.copy()

    df = prepare_dataset(df)
    df['Loan_term_code'] = df['Loan_term'].cat.codes
    df['Goods_category_code'] = df['Goods_category'].cat.codes
    df['Merch_code'] = df['Merch_code'].cat.codes
    df['Family status'] = df['Family status'].cat.codes
    df['education'] = df['education'].cat.codes
    df['employment status'] = df['employment status'].cat.codes
    df['Value'] = df['Value'].cat.codes

    return df


if __name__ == "__main__":
    create_stage("create_features", feature_prepare_in_dataset)