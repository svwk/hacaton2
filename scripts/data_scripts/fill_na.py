#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage
from datetime import date


def fill_na_in_dataset(source_dataset):
    """
    Заполнение пропусков
    :param source_dataset:  Исходный датасет
    """
    df = source_dataset.copy()

    df['Value'] = df['Value'].fillna('Нет стажа')
    df['JobStartDate'] = df['JobStartDate'].fillna(date.today())
    df['gender'] = df['gender'].fillna(df.gender.mode())
    df['Family status'] = df['Family status'].fillna(df['Family status'].mode())
    df['ChildCount'] = df['ChildCount'].fillna(0)


    return df


create_stage("fill_na", fill_na_in_dataset)