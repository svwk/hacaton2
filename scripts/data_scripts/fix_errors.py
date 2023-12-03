#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage


def fix_errors_in_dataset(source_dataset):
    """
    Исправление аномалий
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    return df


create_stage("fix_errors", fix_errors_in_dataset)