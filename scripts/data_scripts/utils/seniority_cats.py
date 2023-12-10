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
    numeric_value = int(numeric_value)

    for key, value_range in seniority_values.items():
        if numeric_value in value_range:
            return key

    return DEFAULT_CAT

    # if numeric_value == 0:
    #     return 'Нет стажа'
    # if 1 <= numeric_value <= 3:
    #     return 'менее 4 месяцев'
    # elif 4 <= numeric_value <= 6:
    #     return '4 - 6 месяцев'
    # elif 6 < numeric_value <= 12:
    #     return '6 месяцев - 1 год'
    # if 12 < numeric_value <= 24:
    #     return '1 - 2 года'
    # elif 24 < numeric_value <= 36:
    #     return '2 - 3 года'
    # elif 36 < numeric_value <= 48:
    #     return '3 - 4 года'
    # elif 48 < numeric_value <= 60:
    #     return '4 - 5 лет'
    # elif 60 < numeric_value <= 72:
    #     return '5 - 6 лет'
    # elif 72 < numeric_value <= 84:
    #     return '6 - 7 лет'
    # elif 84 < numeric_value <= 96:
    #     return '7 - 8 лет'
    # elif 96 < numeric_value <= 108:
    #     return '8 - 9 лет'
    # elif 108 < numeric_value <= 120:
    #     return '9 - 10 лет'
    # elif numeric_value > 120:
    #     return '10 и более лет'


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

    # if str_value == 'Нет стажа':
    #     return 0
    # elif 'менее 4 месяцев' in str_value:
    #     return 3
    # elif '4 - 6 месяцев' in str_value:
    #     return 6
    # elif '6 месяцев - 1 год' in str_value:
    #     return 9
    #
    # words_array = str_value.split(' ')
    # numeric_filtered_array = list(filter(lambda x: x.isdigit(), words_array))
    # numeric_value = min([int(y) for y in numeric_filtered_array]) * 12
    # return numeric_value
