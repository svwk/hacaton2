#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage


def fill_na_in_dataset(source_dataset):
    """
    Заполнение пропусков
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    return df


create_stage("fill_na", fill_na_in_dataset)