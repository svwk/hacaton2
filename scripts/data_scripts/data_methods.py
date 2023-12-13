"""
Общие методы работы с данными
"""
import sys
import os
import pandas as pd
import numpy as np


# project_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir, os.path.pardir))
project_path = os.getcwd()


def create_stage(stage_name, function):
    """
    Выполнение одного из этапов обработки данных
    :param stage_name:
    :param function:
    :return:
    """

    if len(sys.argv) != 2:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write(f"\tpython3 {stage_name}.py data-file\n")
        sys.exit(1)

    f_input = sys.argv[1]

    # %% Задание путей для файлов
    stage_dir = os.path.join(project_path, "data", f"stage_{stage_name}")
    os.makedirs(stage_dir, exist_ok=True)

    # %% Чтение файла данных
    filename_input = os.path.join(project_path, f_input)
    filename_output = os.path.join(stage_dir, "dataset.csv")

    df = pd.read_csv(filename_input, sep=';', parse_dates=['JobStartDate', 'BirthDate'])
    df = function(df)

    # Сохранение DataFrame в файл
    df.to_csv(filename_output, index=False, sep=';')

    return stage_dir


def to_polynom(x, order=2):
    """
    Преобразование к полиному
    :param x: исходные данные
    :param order: степень полинома
    """
    order_range = range(2, order + 1, 1)
    out = np.copy(x)
    for i in order_range:
        out = np.hstack([out, np.power(x, i)])
    return out
