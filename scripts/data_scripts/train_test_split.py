#! python
# -*- coding: UTF-8 -*-

import sys
import os
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split

from data_methods import project_path


def separate_dataset(source_dataset, p_split_ratio, random_state=42):
    """
     Разделение на обучающую и тестовую выборки
    :param p_split_ratio: Отношение для разделения
    :param source_dataset: Исходный датасет
    :param random_state: фиксированный сид случайных чисел (для повторяемости)
    :return: Два дата-фрейма с обучающими и тестовыми данными
    """

    target_columns = ["BankA_decision", "BankB_decision", "BankC_decision", "BankD_decision", "BankE_decision"]

    X = source_dataset.drop(target_columns, axis=1)
    y = source_dataset[target_columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=p_split_ratio, random_state=random_state,
                                                        stratify=y)

    df_train = pd.concat([X_train, y_train], axis=1)
    df_test = pd.concat([X_test, y_test], axis=1)

    return df_train, df_test


stage_name = "train_test_split"
params = yaml.safe_load(open(os.path.join(project_path, "params.yaml")))["split"]
p_split_ratio = params["split_ratio"]
print(p_split_ratio)

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write(f"\tpython3 {stage_name}.py data-file\n")
    sys.exit(1)

f_input = sys.argv[1]

# %% Задание путей для файлов
stage_dir = os.path.join(project_path, "data", f"stage_{stage_name}")

# %% Чтение файла данных
filename_input = os.path.join(project_path, f_input)
train_filename_output = os.path.join(stage_dir, "train.csv")
test_filename_output = os.path.join(stage_dir, "test.csv")

df = pd.read_csv(filename_input, sep=';')
print(f'Строк - {df.shape[0]}')
df_train, df_test = separate_dataset(df, p_split_ratio)

# Сохранение DataFrame в файл
os.makedirs(stage_dir, exist_ok=True)
df_train.to_csv(train_filename_output, index=False, sep=';')
df_test.to_csv(test_filename_output, index=False, sep=';')

