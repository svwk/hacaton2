#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage


def prepare_dataset(source_dataset):
    """
    Начальная подготовка датасета
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    return df


create_stage("data_prepare", prepare_dataset)
