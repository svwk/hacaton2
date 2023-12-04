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

    df = df.dropna(how='all')

    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    mode_gender = df['Gender'].value_counts().idxmax()
    mode_family_status = df['Family status'].value_counts().idxmax()

    df['Value'] = df['Value'].fillna('Нет стажа')
    df['JobStartDate'] = df['JobStartDate'].fillna(date.today())
    df['Gender'] = df['Gender'].fillna(mode_gender)
    df['Family status'] = df['Family status'].fillna(mode_family_status)
    df['ChildCount'] = df['ChildCount'].fillna(0)

    return df


create_stage("fill_na", fill_na_in_dataset)