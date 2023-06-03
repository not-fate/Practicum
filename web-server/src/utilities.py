"""
Модуль вспомогательных функций.

"""
import logging


def log_to_logfile_and_console(text: str) -> None:
    """Вывод служебных сообщений в консоль и в специальный лог-файл [реализация п.п. 6]
    @text - текст логирования.
    """
    logging.info(text)
    print(text)


def parse_http_query(request_line: str) -> tuple[str, str, dict[str, str]]:
    """
    Парсинг HTTP-запроса браузера.
    @request - запрос браузера.
    -> возвращает кортеж (тип запроса, запрашиваемый адрес, словарь заголовков).
    """
    http_headers = dict()
    splited_message = request_line.split('\r\n\r\n')[0].split("\r\n")
    query, headers = splited_message[0], splited_message[1:]
    for _ in headers:
        header = _.split(": ")
        http_headers[header[0]] = header[1]
    request_line = query.split(" ")
    type, url = request_line[0], request_line[1]
    return type, url, http_headers


def validate_filetype(file: str) -> bool:
    """ [Реализация п.п. 6.]
    Проверка, что запрашиваемый файл имеет разрешенный тип.
    """
    correct_filetypes = ["html", "pdf", "png"]
    if not file:
        return False
    if "." not in file:
        return False
    return file.split('.')[1] in correct_filetypes


