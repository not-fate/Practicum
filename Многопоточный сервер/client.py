import socket as _socket
import logging

from helper import log_to_logfile_and_console, validate_port, validate_host


class Client:
    """ Класс, представляющий клиент.
    @socket - клиентский сокет.
    @in_connect - статус подключения,
    т.е. находится ли клиент в соединении с каким-либо сервером.
    @server_port, @server_address - адресные данные сервера, с которым соединен клиент. """

    def __init__(self):
        self.socket = _socket.socket()
        self.in_connect: bool = False
        self.server_port: int = 0
        self.server_address: str = "127.0.0.1"
        logging.basicConfig(format="%(asctime)s - %(message)s",
                            level=logging.INFO, filename="logs/client_log.log",
                            filemode="w")

    def connection_to_server(self, address: str, port: int) -> None:
        """ Попытка соединиться с сервером по переданному адресу.
        @address, @port - адресные данные сервера. """
        try:
            self.socket.connect((address, port))
            log_to_logfile_and_console(f"Соединение с сервером {(address, port)} установлено.")
            self.server_address, self.server_port, self.in_connect = address, port, True
        except OSError as e:
            log_to_logfile_and_console(f"Соединение с сервером установить не удалось. Проверьте данные для "
                                       f"подключения к серверу.\n {e}")

    def send_message(self, message: str) -> None:
        """ Отправка сообщения серверу."""
        self.socket.send(message.encode())
        log_to_logfile_and_console('Отправка сообщение на сервер.')

    def receive_message(self) -> str:
        """ Получение сообщения от сервера. """
        log_to_logfile_and_console(f"Прием данных от сервера {(message := self.socket.recv(1024).decode())}")
        return message

    def stop(self) -> None:
        """ Отключение клиентского сокета. """
        self.socket.close()
        log_to_logfile_and_console("Закрытие соединения.")


if __name__ == "__main__":
    client = Client()
    client.connection_to_server(
        validate_host(input("Введите имя хоста для установки соединения (по умолчанию локально): ")),
        validate_port(input("Введите номер порта (по умолчанию 9090): ")))
    try:
        if client.in_connect:
            while message := input("Введите сообщение для отправки на сервер (пустое сообщение оборвет связь с "
                                   "сервером): "):
                client.send_message(message)
                client.receive_message()
    except Exception as exc:
        print(f"Где-то что-то пошло не так. Ну и ладно. Не грустите, вот вам <3. {exc.args}")
    finally:
        client.stop()
