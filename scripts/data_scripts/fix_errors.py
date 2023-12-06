#! python
# -*- coding: UTF-8 -*-

from data_methods import create_stage
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

#Прожиточный минимум
min_adult = 15669
min_child = 13944

def fix_errors_in_dataset(source_dataset):
    """
    Исправление аномалий
    :param source_dataset:  Исходный датасет
    """

    df = source_dataset.copy()

    df = df.apply(fix_work_age, axis=1)
    df = df.apply(fix_expense, axis=1)

    return df

def fix_expense(raw):
    real_expense = min_adult
    child_expense = min_child * raw['ChildCount']

    if(check_family_status(raw['Family status'])):
        real_expense += min_adult

    real_expense += child_expense

    if(real_expense > raw['MonthExpense']):
        raw['MonthExpense'] = real_expense

    return raw

def check_family_status(status):
  status = str(status)

  if(status == 'Женат / замужем' or status == 'Гражданский брак / совместное проживание'):
    return True
  else:
    return False

def fix_work_age(raw):
  work_age = float(values_to_num(raw['Value']))
  age = time_diff(raw['BirthDate'])

  work_age_from_now_to_start_date = time_diff(raw['JobStartDate'])

  if(age < 23 and work_age < age / 2):
      raw['Value'] = 'Нет стажа'
      return raw

  if(work_age < work_age_from_now_to_start_date):
    work_age = work_age_from_now_to_start_date
    raw['Value'] = num_to_cat(work_age)

  return raw

def values_to_num(line):
    line = str(line)

    if (line == 'Нет стажа'):
        return 0
    elif ('менее 4 месяцев' in line):
        return 0.3
    elif ('4 - 6 месяцев' in line):
        return 0.4
    elif ('6 месяцев' in line):
        return 0.6
    elif ('6 месяцев - 1 год' in line):
        return 0.9

    cur_value = line.split(' ')
    pre_num_value = list(filter(lambda x: try_to_int(x) == True, cur_value))
    num_value = min([int(y) for y in pre_num_value])
    return num_value

def try_to_int(array_el):
    try:
        converted = int(array_el)
        return True
    except:
        return False

def num_to_cat(num):
    if (num == 0):
        return 'Нет стажа'
    elif (num == 0.3):
        return 'Нет стажа'
    elif (num == 0.4):
        return '4 - 6 месяцев'
    elif (num == 0.6):
        return '6 месяцев'
    elif (num == 0.9):
        return '6 месяцев - 1 год'

    if (num == 1):
        return '1 - 2 года'
    elif (num >= 2 and num < 3):
        return '2 - 3 года'
    elif (num >= 3 and num < 4):
        return '3 - 4 года'
    elif (num >= 4 and num < 5):
        return '4 - 5 лет'
    elif (num >= 5 and num < 6):
        return '5 - 6 лет'
    elif (num >= 6 and num < 7):
        return '6 - 7 лет'
    elif (num >= 7 and num < 8):
        return '7 - 8 лет'
    elif (num >= 8 and num < 9):
        return '8 - 9 лет'
    elif (num >= 9 and num < 10):
        return '6 месяцев - 1 год'
    elif (num >= 10):
        return '9 - 10 лет'

def time_diff(d):
  d = str(d)
  date_only = d.split(' ')

  if(len(date_only) > 1):
    del date_only[1]

  start = datetime.fromisoformat(str(date_only[0]))
  from_now_to_start_job = datetime.now() - start

  return float(from_now_to_start_job.days / 365)

create_stage("fix_errors", fix_errors_in_dataset)