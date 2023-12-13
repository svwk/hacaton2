#! python
# -*- coding: UTF-8 -*-

import sys
import os
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split

from data_methods import project_path


def separate_bank_dataset(source_dataset, p_split_ratio, bank_id, random_state=42):
    """
     Разделение на обучающую и тестовую выборки для каждого банка по отдельности
    :param p_split_ratio: Отношение для разделения
    :param source_dataset: Исходный датасет
    :param bank_id: идентификатор банка
    :param random_state: фиксированный сид случайных чисел (для повторяемости)
    :return: Два дата-фрейма с обучающими и тестовыми данными
    """
    target_column = "решение банка "+bank_id
    bank_columns = ["решение банка A", "решение банка B", "решение банка C", "решение банка D", "решение банка E"]

    source_dataset = source_dataset[source_dataset[target_column] != 'error']

    X = source_dataset.drop(bank_columns, axis=1)
    y = source_dataset[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=p_split_ratio, random_state=random_state,
                                                        stratify=y)

    df_train = pd.concat([X_train, y_train], axis=1)
    df_test = pd.concat([X_test, y_test], axis=1)

    return df_train, df_test


stage_name = "train_test_split"
params = yaml.safe_load(open(os.path.join(project_path, "params.yaml")))["split"]
split_ratio = params["split_ratio"]
bank_id = params["bank_id"]

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write(f"\tpython3 {stage_name}.py data-file\n")
    sys.exit(1)

f_input = sys.argv[1]

# %% Задание путей для файлов
stage_dir = os.path.join(project_path, "data", f"stage_{stage_name}")

# %% Чтение файла данных
filename_input = os.path.join(project_path, f_input)

df = pd.read_csv(filename_input, sep=';')
print(f'Строк - {df.shape[0]}')

# Сохранение DataFrame в файл
os.makedirs(stage_dir, exist_ok=True)

for bank in bank_id_list:
    df_train, df_test = separate_bank_dataset(df, split_ratio, bank)
    train_filename_output = os.path.join(stage_dir, "train_" + bank + ".csv")
    test_filename_output = os.path.join(stage_dir, "test_" + bank + ".csv")
    df_train.to_csv(train_filename_output, index=False, sep=';')
    df_test.to_csv(test_filename_output, index=False, sep=';')
