#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import utils.seniority_cats as sc


def create_features_in_dataset(source_dataset):
    """
    Создание новых признаков и удаление ненужных
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    # Создание новых числовых признаков

    df['Имеет_доход'] = ((pd.notna(df['JobStartDate'])) & (df['employment status'] != "Не работаю")).astype('int')
    # df['Имеет_доход'] = df['Имеет_доход'].astype('int')

    df['Кредитная_нагрузка'] = (df['MonthProfit'] - df['MonthExpense']) / (df['Loan_amount'] / df['Loan_term'])
    # df['Кредитная_нагрузка'] = np.where(df['Кредитная_нагрузка'] < 0, 0, df['Кредитная_нагрузка'])
    df['Кредит_возможен'] = np.where(df['Кредитная_нагрузка'] > 1.25, 1, 0)

    df['Возраст'] = df['BirthDate'].apply(lambda r: relativedelta(datetime.today(), r).years)

    # Стаж работы на последнем месте в месяцах
    last_seniority = df.apply(sc.set_last_seniority_new_cat, axis=1)
    df['Последний_стаж_работы'] = pd.Categorical(last_seniority, ordered=True,
                                                 categories=['Нет стажа', 'Менее  6 месяцев', 'Менее 2 лет',
                                                             'Менее 5 лет', 'Менее 10 лет', '10 и более лет']
                                                 )
    last_seniority = pd.get_dummies(df['Последний_стаж_работы'], prefix="Посл_стаж", dtype=int)
    df['Код_Последний_стаж_работы'] = df['Последний_стаж_работы'].cat.codes

    # Создание новых категориальных признаков

    df['Категория_товара'] = pd.Categorical(df['Goods_category'], ordered=True)
    df['Код_Категория_товара'] = df['Категория_товара'].cat.codes
    goods_category = pd.get_dummies(df['Категория_товара'], prefix="Кат_товара", dtype=int)

    merch_code = pd.get_dummies(df['Merch_code'], prefix="код_магазина", dtype=int)

    df['Family status'] = df['Family status'].apply(replace_family_status)
    df['Семейное_положение'] = pd.Categorical(df['Family status'], ordered=True)
    df['Код_Семейное_положение'] = df['Семейное_положение'].cat.codes
    family_status = pd.get_dummies(df['Семейное_положение'], prefix="Сем_положение", dtype=int)

    df['education'] = df['education'].apply(replace_education)
    df['Образование'] = pd.Categorical(df['education'], ordered=True,
                                       categories=['Среднее', 'Среднее профессиональное', 'Высшее']
                                       )
    df['Код_Образование'] = df['Образование'].cat.codes
    education = pd.get_dummies(df['Образование'], prefix="Образование", dtype=int)

    df['employment status'] = df['employment status'].apply(replace_employment_status)
    df['Тип_занятости'] = pd.Categorical(df['employment status'], ordered=True)
    df['Код_Тип_занятости'] = df['Тип_занятости'].cat.codes
    employment_status = pd.get_dummies(df['Тип_занятости'], prefix="Занятость", dtype=int)

    df['Value'] = df['Value'].apply(replace_seniority)
    df['Стаж_работы'] = pd.Categorical(df['Value'], ordered=True,
                                       categories=['Нет стажа', 'Менее  6 месяцев', 'Менее 2 лет', 'Менее 5 лет',
                                                   'Менее 10 лет', '10 и более лет'])
    df['Код_Стаж_работы'] = df['Стаж_работы'].cat.codes
    value = pd.get_dummies(df['Стаж_работы'], prefix="Общий_стаж", dtype=int)

    df['Срок_кредита'] = pd.Categorical(df['Loan_term'], ordered=True)
    loan_term = pd.get_dummies(df['Срок_кредита'], prefix="Срок_кредита", dtype=int)

    df['Колво_детей'] = df['ChildCount'].apply(replace_childcount)
    df['Колво_детей'] = pd.Categorical(df['Колво_детей'], ordered=True,
                                       categories=['Без детей', '1 ребенок', '2 и более детей'])
    df['Код_Колво_детей'] = df['Колво_детей'].cat.codes
    child_count = pd.get_dummies(df['Колво_детей'], prefix="Колво_детей", dtype=int)

    df = pd.concat(
        [df, value, education, employment_status, family_status, loan_term, goods_category,
         merch_code, last_seniority, child_count],
        axis=1
    )

    df['Решение_банка_A'] = pd.Categorical(df['BankA_decision'], categories=['denied', 'success', 'error'],
                                           ordered=True)
    df['Решение_банка_B'] = pd.Categorical(df['BankB_decision'], categories=['denied', 'success', 'error'],
                                           ordered=True)
    df['Решение_банка_C'] = pd.Categorical(df['BankC_decision'], categories=['denied', 'success', 'error'],
                                           ordered=True)
    df['Решение_банка_D'] = pd.Categorical(df['BankD_decision'], categories=['denied', 'success', 'error'],
                                           ordered=True)
    df['Решение_банка_E'] = pd.Categorical(df['BankE_decision'], categories=['denied', 'success', 'error'],
                                           ordered=True)

    df['Решение_банка_A'] = df['Решение_банка_A'].cat.codes
    df['Решение_банка_B'] = df['Решение_банка_B'].cat.codes
    df['Решение_банка_C'] = df['Решение_банка_C'].cat.codes
    df['Решение_банка_D'] = df['Решение_банка_D'].cat.codes
    df['Решение_банка_E'] = df['Решение_банка_E'].cat.codes

    df = df.drop(columns=['BirthDate', 'JobStartDate', 'Goods_category',
                          'Family status', 'education', 'employment status', 'Value', 'Loan_term',
                          'ChildCount', 'BankA_decision', 'BankB_decision', 'BankC_decision',
                          'BankD_decision', 'BankE_decision'])

    df = df.rename(columns={
        'MonthProfit': 'Ежемесячный_доход',
        'MonthExpense': 'Ежемесячный_расход',
        'Loan_amount': 'Сумма_заказа',
        'Merch_code': 'Код_магазина',
        'Gender': 'Пол',
        'SNILS': 'СНИЛС'
    })

    return df


def replace_family_status(old_value):
    """
    Заменяет старое значение категории признака 'Семейное_положение' на новое
    :param old_value: старое значение категории признака 'Семейное_положение'
    :return: новое значение категории признака 'Семейное_положение'
    """

    if old_value == 'Гражданский брак / совместное проживание':
        return 'Женат / замужем'
    if old_value == 'Вдовец / вдова':
        return 'Разведён / Разведена'
    return old_value


def replace_education(old_value):
    """
    Заменяет старое значение категории признака 'Образование' на новое
    :param old_value: старое значение категории признака 'Образование'
    :return: новое значение категории признака 'Образование'
    """
    if old_value in ['Высшее - специалист', 'Бакалавр', 'Магистр', 'Несколько высших']:
        return 'Высшее'
    if old_value in ['Неоконченное среднее', 'Среднее', 'Неоконченное высшее']:
        return 'Среднее'
    return old_value


def replace_employment_status(old_value):
    """
    Заменяет старое значение категории признака 'Тип_занятости' на новое
    :param old_value: старое значение категории признака 'Тип_занятости'
    :return: новое значение категории признака 'Тип_занятости'
    """
    if old_value in ['Работаю по найму полный рабочий день/служу', 'Работаю по найму неполный рабочий день']:
        return 'Работаю по найму'
    if old_value in ['Пенсионер', 'Студент', 'Декретный отпуск', 'Не работаю']:
        return 'Иные виды'
    return old_value


def replace_childcount(old_value):
    """
    Заменяет старое значение категории признака 'ChildCount' на новое
    :param old_value: старое значение категории признака 'ChildCount'
    :return: новое значение категории признака 'ChildCount'
    """
    if old_value == 0:
        return 'Без детей'
    if old_value == 1:
        return '1 ребенок'
    return '2 и более детей'


def replace_seniority(old_value):
    """
    Заменяет старое значение категории признака 'стаж работы' на новое
    :param old_value: старое значение категории признака 'стаж работы'
    :return: новое значение категории признака 'стаж работы'
    """
    # Общий стаж в месяцах
    total_seniority_in_months = int(sc.seniority_cat_to_month_count(old_value))
    return sc.months_seniority_to_new_cat(total_seniority_in_months)


if __name__ == "__main__":
    create_stage("create_features", create_features_in_dataset)
