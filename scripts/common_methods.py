from scripts import message_constants as mc

def print_error(ex, file_path):
    """
    Вывод сообщения об ошибке сохранения файла
    :param ex: объект исключения
    :param file_path:  полный путь файла
    """
    print(f"{mc.FILE_SAVE_ERROR} {file_path}: {ex.args}")