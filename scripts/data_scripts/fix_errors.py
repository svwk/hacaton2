#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

#Прожиточный минимум
ADULT_LIVING_WAGE = 15669
CHILD_LIVING_WAGE = 13944

def fix_errors_in_dataset(source_dataset):
    """
    Исправление аномалий
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    df = df.apply(fix_work_age, axis=1)
    df = df.apply(fix_expense, axis=1)

    return df

def fix_expense(application):
    """
    Исправление аномалий в столбце с тратами
    :param application:  Данные заявки
    """

    real_expense = ADULT_LIVING_WAGE
    child_expense = CHILD_LIVING_WAGE * application['ChildCount']

    if(check_family_status(application['Family status'])):
        real_expense += ADULT_LIVING_WAGE

    real_expense += child_expense

    if(real_expense > application['MonthExpense']):
        application['MonthExpense'] = real_expense

    return application

def check_family_status(status):
    """
        Проверка семейного статуса, если замужем или женат вернуть True
        :param status:  Данные из заявки
    """
    status = str(status)

    if(status == 'Женат / замужем' or status == 'Гражданский брак / совместное проживание'):
        return True
    else:
        return False

def fix_work_age(application):
    """
    Исправление аномалий в столбце со стажем работы
    :param application:  Данные заявки
    """

    #Общий стаж
    work_age = int(values_to_num(application['Value']))

    #Возраст
    age = time_diff(application['BirthDate'])

    #Стаж работы на последнем месте
    work_age_from_now_to_start_date = time_diff(application['JobStartDate'])

    #Проверка на соотвествие трудовому зк
    if(age < 16):
        application['Value'] = 'Нет стажа'
        return application

    #Стаж на последнем рабочем месте не может быть больше чем возраст - 16 (ЗК)
    work_age_from_now_to_start_date = min(work_age_from_now_to_start_date, age - 16)
    #Так же как и общий стаж
    work_age = max(work_age, age - 16)

    #Общий стаж не может быть меньше, чем стаж на последнем рабочем месте
    work_age = min(work_age, work_age_from_now_to_start_date)

    application['Value'] = num_to_cat(work_age)
    return application


def values_to_num(str_value):
    """
    Конвертация категориального значения стажа в числовой
    :param str_value:  Данные из заявки
    """

    str_value = str(str_value)

    if (str_value == 'Нет стажа'):
        return 0
    elif ('менее 4 месяцев' in str_value):
        return 3
    elif ('4 - 6 месяцев' in str_value):
        return 4
    elif ('6 месяцев' in str_value):
        return 6
    elif ('6 месяцев - 1 год' in str_value):
        return 9

    words_array = str_value.split(' ')
    numeric_filtered_array = list(filter(lambda x: try_to_int(x) == True, words_array))
    numeric_value = min([int(y) for y in numeric_filtered_array]) * 12
    return numeric_value

def try_to_int(array_el):
    """
    Проверка строки на возможность конвертации в число
    :param array_el:  Элемент массива
    """
    try:
        converted = int(array_el)
        return True
    except:
        return False

def num_to_cat(numeric_value):
    """
    Конвертация числового значения стажа в категориальный
    :param str_value:  Данные из заявки
    """
    if (numeric_value == 0):
        return 'Нет стажа'
    elif (numeric_value == 3):
        return 'Нет стажа'
    elif (numeric_value == 4):
        return '4 - 6 месяцев'
    elif (numeric_value == 6):
        return '6 месяцев'
    elif (numeric_value == 9):
        return '6 месяцев - 1 год'

    if (numeric_value >= 12 and numeric_value < 24):
        return '1 - 2 года'
    elif (numeric_value >= 24 and numeric_value < 36):
        return '2 - 3 года'
    elif (numeric_value >= 36 and numeric_value < 48):
        return '3 - 4 года'
    elif (numeric_value >= 48 and numeric_value < 60):
        return '4 - 5 лет'
    elif (numeric_value >= 60 and numeric_value < 72):
        return '5 - 6 лет'
    elif (numeric_value >= 72 and numeric_value < 84):
        return '6 - 7 лет'
    elif (numeric_value >= 84 and numeric_value < 96):
        return '7 - 8 лет'
    elif (numeric_value >= 96 and numeric_value < 108):
        return '8 - 9 лет'
    elif (numeric_value >= 108 and numeric_value < 120):
        return '9 - 10 лет'
    elif (numeric_value >= 120):
        return '10 и более лет'

def time_diff(date):
    from_now_to_start_job = datetime.now() - date
    return int(from_now_to_start_job.days / 30)

create_stage("fix_errors", fix_errors_in_dataset)