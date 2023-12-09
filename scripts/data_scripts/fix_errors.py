#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from data_prepare import prepare_dataset
from utils.num_to_cat import num_to_cat

# Прожиточный минимум
ADULT_LIVING_WAGE = 15669
CHILD_LIVING_WAGE = 13944


def fix_errors_in_dataset(source_dataset):
    """
    Исправление аномалий в данных
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()
    df = prepare_dataset(df)

    df = df.apply(fix_seniority, axis=1)
    df = df.apply(fix_expense, axis=1)

    return df


def fix_expense(application_data):
    """
    Исправление аномальных значений расхода семьи
    :param application_data:  Данные заявки пользователя
    """

    # Реальный расход пользователя, если он один в семье
    real_expense = ADULT_LIVING_WAGE

    # Расходы на содержание супруга/супруги при наличии
    if check_family_status(application_data['Family status']):
        real_expense += ADULT_LIVING_WAGE

    # Расходы на содержание детей
    real_expense += CHILD_LIVING_WAGE * application_data['ChildCount']

    # Если рассчитанные расходы превышают указанные в заявлении,
    # исправляем на большее значение
    if real_expense > application_data['MonthExpense']:
        application_data['MonthExpense'] = real_expense

    return application_data


def check_family_status(status):
    """
        Проверка семейного положения, при наличии супруга/супруги
         возвращает True
        :param status:  Данные из заявки
    """
    status = str(status)

    if (status == 'Женат / замужем' or
            status == 'Гражданский брак / совместное проживание'):
        return True
    else:
        return False


def fix_seniority(application_data):
    """
    Исправление аномальных значений стажа работы
    :param application_data:  Данные заявки
    """

    # Общий стаж в месяцах
    total_seniority_in_months = int(values_to_num(application_data['Value']))

    # Возраст
    age = relativedelta(datetime.today(), application_data['BirthDate'])

    # Максимально возможный трудовой стаж в месяцах
    # (возраст - 16) (ТК)
    max_seniority_in_months = age.months + (age.years - 16) * 12

    # Стаж работы на последнем месте
    last_seniority = relativedelta(datetime.today(), application_data['JobStartDate'])

    # Стаж работы на последнем месте в месяцах
    last_seniority_in_months = last_seniority.months + last_seniority.years * 12

    # Проверка на соответствие трудовому законодательству
    if age.years < 16:
        application_data['Value'] = 'Нет стажа'
        return application_data

    # Стаж на последнем рабочем месте не может быть больше,
    # чем максимально возможный трудовой стаж
    new_last_seniority = min(last_seniority_in_months, max_seniority_in_months)

    # Общий стаж не может быть больше,
    # чем максимально возможный трудовой стаж
    new_total_seniority = min(total_seniority_in_months, max_seniority_in_months)

    # Общий стаж не может быть меньше, чем стаж на последнем рабочем  месте
    new_total_seniority = max(new_total_seniority, new_last_seniority)

    if new_last_seniority != last_seniority_in_months:
        application_data['JobStartDate'] = datetime.strftime((date.today() -
                                            relativedelta(months=new_last_seniority)), "%Y-%m-%d %H:%M:%S")

    if new_total_seniority != total_seniority_in_months:
        application_data['Value'] = num_to_cat(new_total_seniority)

    return application_data


def values_to_num(str_value):
    """
    Конвертация категориального значения стажа в целое число
    :param str_value:  Данные из заявки
    """

    str_value = str(str_value)

    if str_value == 'Нет стажа':
        return 0
    elif 'менее 4 месяцев' in str_value:
        return 3
    elif '4 - 6 месяцев' in str_value:
        return 4
    elif '6 месяцев' in str_value:
        return 6
    elif '6 месяцев - 1 год' in str_value:
        return 9

    words_array = str_value.split(' ')
    numeric_filtered_array = list(filter(lambda x: x.isdigit(), words_array))
    numeric_value = min([int(y) for y in numeric_filtered_array]) * 12
    return numeric_value



def time_diff(date_value):
    """
    Определяет разницу между некоторой датой и текущей
    в месяцах
    :param date_value: Дата, для которой необходимо найти разницу
    """

    from_now_to_start_job = datetime.today() - date_value

    return int(from_now_to_start_job.days / 30)


if __name__ == "__main__":
    create_stage("fix_errors", fix_errors_in_dataset)
