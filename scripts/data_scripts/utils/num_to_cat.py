
def num_to_cat(numeric_value):
    """
    Конвертация числового значения стажа в категориальный
    :param numeric_value:
    :param str_value:  Данные из заявки
    """
    if numeric_value == 0:
        return 'Нет стажа'
    elif numeric_value == 3:
        return 'Нет стажа'
    elif numeric_value == 4:
        return '4 - 6 месяцев'
    elif numeric_value == 6:
        return '6 месяцев'
    elif numeric_value == 9:
        return '6 месяцев - 1 год'

    if 12 <= numeric_value < 24:
        return '1 - 2 года'
    elif 24 <= numeric_value < 36:
        return '2 - 3 года'
    elif 36 <= numeric_value < 48:
        return '3 - 4 года'
    elif 48 <= numeric_value < 60:
        return '4 - 5 лет'
    elif 60 <= numeric_value < 72:
        return '5 - 6 лет'
    elif 72 <= numeric_value < 84:
        return '6 - 7 лет'
    elif 84 <= numeric_value < 96:
        return '7 - 8 лет'
    elif 96 <= numeric_value < 108:
        return '8 - 9 лет'
    elif 108 <= numeric_value < 120:
        return '9 - 10 лет'
    elif numeric_value >= 120:
        return '10 и более лет'
