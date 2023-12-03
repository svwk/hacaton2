#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage


def create_features_in_dataset(source_dataset):
    """
    Создание новых признаков и удаление ненужных
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    return df


create_stage("create_features", create_features_in_dataset)