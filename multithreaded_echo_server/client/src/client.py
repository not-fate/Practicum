import socket as _socket
import logging

from utilities import log_to_logfile_and_console, validate_port, validate_host

logging.basicConfig(format="%(asctime)s - %(message)s",
                    level=logging.INFO, filename="client/src/logs.log",
                    filemode="w")


class Client:
    """ Класс, представляющий клиент.

    @socket - клиентский сокет.
    @in_connect - статус подключения,
    т.е. находится ли клиент в соединении с каким-либо сервером.
    @server_port, @server_address - адресные данные сервера, с которым соединен клиент.

    """

    def __init__(self):
        self.socket = _socket.socket()
        self.in_connect: bool = False
        self.server_port: int = 0
        self.server_address: str = "127.0.0.1"

    def connection_to_server(self, address: str, port: int) -> None:
        """ Попытка соединиться с сервером по переданному адресу.
        @address, @port - адресные данные сервера. """
        try:
            self.socket.connect((address, port))
            log_to_logfile_and_console(f"\n\033[34m\033[3m-> Соединение с сервером {(address, port)} установлено.\033[0m\n")
            self.server_address, self.server_port, self.in_connect = address, port, True
        except OSError as e:
            log_to_logfile_and_console(f"Соединение с сервером установить не удалось. Проверьте данные для "
                                       f"подключения к серверу.\n {e}")

    def send_message(self, message: str) -> None:
        """ Отправка сообщения серверу. """
        self.socket.send(message.encode())
        log_to_logfile_and_console('...отправка сообщения на сервер...')

    def receive_message(self) -> str:
        """ Получение сообщения от сервера. """
        message: str = self.socket.recv(1024).decode()
        log_to_logfile_and_console(f"Прием данных от сервера: {message}.\n")
        return message

    def stop(self) -> None:
        """ Отключение клиентского сокета. """
        self.socket.close()
        log_to_logfile_and_console("\033[34m\033[3m-> Закрытие соединения.\033[0m\n")


if __name__ == "__main__":
    client = Client()
    client.connection_to_server(
        validate_host(input("Введите имя хоста для установки соединения (по умолчанию локально): ")),
        validate_port(input("Введите номер порта (по умолчанию 9090): ")))
    try:
        if client.in_connect:
            while message := input("Введите сообщение для отправки на сервер "
                                   "(сообщение 'exit' или пустое сообщение оборвет связь с сервером): "):
                client.send_message(message)
                client.receive_message()
    except Exception as exc:
        print(f"Ошибка: {exc.args}")
    finally:
        client.stop()
