#! python
# -*- coding: UTF-8 -*-

import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import yaml
import sys
import os

all_drop_columns = {
    'A': ['Кат_товара_Education', 'Кат_товара_Education', 'Кат_товара_Other',
          'Занятость_Иные виды', 'Срок_кредита_18', 'Срок_кредита_24'],
    'B': ['Кат_товара_Education', 'Кат_товара_Travel', 'Кат_товара_Furniture',
          'Кат_товара_Education', 'Занятость_Иные виды', 'Срок_кредита_12',
          'Срок_кредита_6'],
    'C': ['Кат_товара_Travel', 'Кат_товара_Furniture', 'Кат_товара_Other',
          'Занятость_Собственное дело', 'Занятость_Иные виды', 'Занятость_Работаю по найму',
          'Срок_кредита_12', 'Срок_кредита_24'],
    'D': ['Кат_товара_Education', 'Кат_товара_Furniture', 'Кат_товара_Education',
          'Занятость_Собственное дело', 'Занятость_Работаю по найму',
          'Срок_кредита_12', 'Срок_кредита_24', 'Срок_кредита_6'],
    'E': ['Кат_товара_Other', 'Срок_кредита_18', 'Срок_кредита_24'],
}


def feature_prepare_for_bank(dataset, data_id, scaler, transform_columns):
    """

    :param dataset:
    :param data_id: идентификатор банка
    :param scaler:
    :param transform_columns:
    :return:
    """

    polynom_order = 3

    dataset = dataset.drop(columns=['Последний_стаж_работы', 'Код_Последний_стаж_работы',
                                    'Категория_товара', 'Код_Категория_товара',
                                    'Код_магазина', 'Семейное_положение', 'Код_Семейное_положение',
                                    'Образование', 'Код_Образование', 'Тип_занятости', 'Код_Тип_занятости',
                                    'Стаж_работы', 'Код_Стаж_работы', 'Срок_кредита', 'Колво_детей',
                                    'Код_Колво_детей'])
    bank_drop_columns = all_drop_columns.get(data_id, [])
    dataset = dataset.drop(columns=bank_drop_columns)

    dataset['Возраст'] = dataset['Возраст'] / 100

    scaled = scaler.transform(dataset[transform_columns])
    scaled = to_polynom(scaled, order=polynom_order)
    dataset = dataset.drop(columns=transform_columns)

    ext_transform_columns = transform_columns.copy()
    for o in range(2, polynom_order + 1):
        for el in transform_columns:
            ext_transform_columns = np.append(ext_transform_columns, f'{el}_{o}')
    # num_columns = np.hstack([num_columns, ['ЕД2', 'ЕР2', 'СЗ2', 'КН2', 'ЕД3', 'ЕР3', 'СЗ3', 'КН3', ]])

    df_standard = pd.DataFrame(scaled, columns=ext_transform_columns)
    dataset = pd.concat([dataset, df_standard], axis=1)

    return dataset


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


if __name__ == "__main__":
    stage_name = "feature_prepare"

    if len(sys.argv) != 2:
        sys.stderr.write("Arguments error. Usage:\n")
        sys.stderr.write(f"\tpython3 {stage_name}.py data-file\n")
        sys.exit(1)

    f_input = sys.argv[1]

    # %% Задание путей для файлов
    project_path = os.getcwd()
    stage_dir = os.path.join(project_path, "data", f"stage_{stage_name}")
    model_dir = os.path.join(project_path, "models")

    # %% Создание каталогов
    os.makedirs(stage_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    params = yaml.safe_load(open(os.path.join(project_path, "params.yaml")))["general"]
    bank_id = params["bank_id"]

    # %% Чтение файла данных
    filename_input = os.path.join(project_path, f_input)
    filename_output = os.path.join(stage_dir, f"dataset_{bank_id}.csv")

    scaler_filename = f'scaler_{bank_id}.pkl'
    scaler_full_filename = os.path.join(model_dir, scaler_filename)

    df = pd.read_csv(filename_input, sep=';')

    target = f'Решение_банка_{bank_id}'
    num_columns = ['Ежемесячный_доход', 'Ежемесячный_расход', 'Сумма_заказа', 'Кредитная_нагрузка']

    df = df.drop(df[(df[target] == 2)].index)
    df = df.reset_index(drop=True)
    df = df.rename(columns={target: 'Y'})
    df = df.drop(columns=[column for column in df.columns
            if column.startswith("Решение_банка")])

    standard_scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    standard_scaler.fit(df[num_columns])
    joblib.dump(standard_scaler, scaler_full_filename)

    df = feature_prepare_for_bank(df, bank_id, standard_scaler, num_columns)

    # Сохранение DataFrame в файл
    df.to_csv(filename_output, index=False, sep=';')
