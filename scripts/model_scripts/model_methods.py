"""
Методы работы с моделью
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from scripts import message_constants as mc

# %% Загрузим, обучим и сохраним модель
def train_model(train_dataset):
    """
    Обучение модели
    :param train_dataset:  Обучающий набор данных
    """

    target_column_name = "z"
    y_train = train_dataset[target_column_name].values
    x_train = train_dataset.drop(target_column_name, axis=1).values

    model = LogisticRegression(max_iter=100_000).fit(x_train, y_train)

    return model


def test_model(test_dataset, model):
    """
    Проверка модели
    :param test_dataset:  Тестовый набор данных
    :param model: Проверяемая модель
    """
    target_column_name = "z"
    y_test = test_dataset[target_column_name].values
    xy_test = test_dataset.drop(target_column_name, axis=1).values

    accuracy = model.score(xy_test, y_test)
    print(f'{mc.MODEL_TEST_ACCURACY}: {accuracy:.3f}')

    return accuracy