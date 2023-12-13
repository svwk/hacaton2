#! python
# -*- coding: UTF-8 -*-

import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import yaml
import os

import data_methods as dm


def feature_prepare_in_dataset(source_dataset, stage_dir):
    """
    Создание новых признаков и удаление ненужных
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()
    df['Возраст'] = df['Возраст'] / 100

    params = yaml.safe_load(open(os.path.join(dm.project_path, "params.yaml")))["split"]
    bank_id = params["bank_id"]

    scaler_filename = f'{bank_id}_scaler.pkl'
    scaler_full_filename = os.path.join(dm.project_path, 'models', scaler_filename)

    num_columns = ['Ежемесячный_доход', 'Ежемесячный_расход', 'Сумма_заказа', 'Кредитная_нагрузка']

    scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(df[num_columns])
    joblib.dump(scaler, scaler_full_filename)

    scaled = scaler.transform(df[num_columns])
    scaled = dm.to_polynom(scaled, order=3)

    num_columns = np.hstack([num_columns, ['ЕД2', 'ЕР2', 'СЗ2', 'КН2', 'ЕД3', 'ЕР3', 'СЗ3', 'КН3', ]])

    df_standard = pd.DataFrame(scaled, columns=num_columns)

    df = df.drop(columns=['Последний_стаж_работы', 'Код_Последний_стаж_работы',
                          'Категория_товара', 'Код_Категория_товара',
                          'Код_магазина', 'Семейное_положение', 'Код_Семейное_положение',
                          'Образование', 'Код_Образование', 'Тип_занятости', 'Код_Тип_занятости',
                          'Стаж_работы', 'Код_Стаж_работы', 'Срок_кредита', 'Колво_детей',
                          'Код_Колво_детей', 'Ежемесячный_доход', 'Ежемесячный_расход', 'Сумма_заказа',
                          'Кредитная_нагрузка'])

    df = pd.concat([df, df_standard], axis=1)

    return df


if __name__ == "__main__":
    stage_dir = dm.create_stage("create_features", feature_prepare_in_dataset)
