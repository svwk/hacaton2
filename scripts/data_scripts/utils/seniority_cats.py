import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

DEFAULT_CAT = 'Нет стажа'

seniority_values = {
    'Нет стажа': range(0, 1),
    'менее 4 месяцев': range(1, 4),
    '4 - 6 месяцев': range(4, 6),
    '6 месяцев - 1 год': range(6, 12),
    '1 - 2 года': range(12, 24),
    '2 - 3 года': range(24, 36),
    '3 - 4 года': range(36, 48),
    '4 - 5 лет': range(48, 60),
    '5 - 6 лет': range(60, 72),
    '6 - 7 лет': range(72, 84),
    '7 - 8 лет': range(84, 96),
    '8 - 9 лет': range(96, 108),
    '9 - 10 лет': range(108, 120),
    '10 и более лет': range(120, 1000),
}


def months_seniority_to_cat(numeric_value):
    """
    Конвертация числового значения стажа в строковое
    представление категории стажа
    :param numeric_value: стаж (количество месяцев)
    :return строковое представление категории стажа
    """
    if numeric_value is None:
        return None

    numeric_value = int(numeric_value)

    for key, value_range in seniority_values.items():
        if numeric_value in value_range:
            return key

    return DEFAULT_CAT


def seniority_cat_to_month_count(str_value):
    """
    Конвертация строкового представления категории стажа
    в количество месяцев
    :param str_value:  строковое представление категории стажа
    :return стаж (количество месяцев)
    """

    str_value = str(str_value)
    range_value = seniority_values.get(str_value, seniority_values[DEFAULT_CAT])

    return max(range_value)


def set_last_seniority(application_data):
    if not pd.isna(application_data['JobStartDate']):
        last_seniority = relativedelta(datetime.today(), application_data['JobStartDate'])
        # Стаж работы на последнем месте в месяцах
        return last_seniority.months + last_seniority.years * 12

    return None


def set_last_seniority_cat(application_data):
    last_seniority = set_last_seniority(application_data)

    return months_seniority_to_cat(last_seniority)

