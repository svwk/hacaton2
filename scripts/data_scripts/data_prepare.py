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

    df['BirthDate'] = pd.to_datetime(df['BirthDate'])
    df['JobStartDate'] = pd.to_datetime(df['JobStartDate'])
    df['Gender'] = np.where(df['Gender'] > 0, 1, 0)
    df['ChildCount'] = df['ChildCount'].fillna(0).astype('int')
    df['SNILS'] = df['SNILS'].fillna(0).astype('int')

    return df


if __name__ == "__main__":
    create_stage("data_prepare", prepare_dataset)
