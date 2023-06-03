"""
Модуль вспомогательных функций.
"""
import logging
import re
from enum import IntEnum


class MType(IntEnum):
    """ Enum для идентификации типа сообщения.
    ~
    Скорее всего, не пригодится."""
    Echo = 1
    WhoIs = 5
    WhoLogin = 6
    WhoHello = 7
    Session = 10
    NotAuth = 20
    AuthData = 21
    AuthOk = 30


def validate_port(port: str) -> int:
    """ Валидация произвольного порта.
    При некорректных данных возвращается 9090 порт.
    @port - произвольный порт."""
    return int(port) if port.isdigit() and 1 < int(
        port) < 65535 else 9090


def validate_host(host: str) -> str:
    """ Валидация имени хоста.
    При некорректных данных возвращается локальный адрес.
    @host - имя хоста.

    """
    return host if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\w*$", host) else "127.0.0.1"


def log_to_logfile_and_console(text: str) -> None:
    """Вывод служебных сообщений в консоль и в специальный лог-файл.
    @text - текст логирования.
    """
    logging.info(text)
    print(text)


def clear_logfile(log: str) -> None:
    """ [Реализация п.п. 4.2 ~multithreaded-echo-server]. Очистка лог-файла. """
    with open(log, "r+") as log:
        log.truncate()


def show_logfile(log: str) -> None:
    """ [Реализация п.п. 4.4 ~multithreaded-echo-server]. Показ лог-файла в консоль. """
    with open(log, "r") as log:
        print(*log.readlines(), sep="\n")
