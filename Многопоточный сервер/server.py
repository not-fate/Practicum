import logging
import socket as _socket
from threading import Thread

from ConnectedClient import ConnectedClient
from helper import *


class Server:
    """ Класс, представляющий сервер.
    @port - номер порта.
    @host - имя.
    @connected_clients - список подключенных к серверу клиентов.
    @socket - сокет для последующего соединения с клиентами. """

    def __init__(self):
        self.port: int = 0
        self.host: str = "127.0.0.1"
        self.connected_clients: list[ConnectedClient] = []
        self.socket: _socket = _socket.socket()
        logging.basicConfig(format="%(asctime)s - %(message)s",
                            level=logging.INFO, filename="logs/server_log.log",
                            filemode="w")
        log_to_logfile_and_console(f"Сервер запущен.")

    def bind_socket(self, port: int) -> None:
        """ [Реализация п.п. 4, 6].
        По умолчанию система назначает серверу любой свободный порт.
        Благодаря данному методу пользователь может попытаться назначить определенный порт.
        @port - произвольный порт. """
        try:
            self.socket.bind((self.host, port))
            log_to_logfile_and_console(f"К сокету привязан порт: {self.socket.getsockname()}")
        except OSError:
            self.socket.bind((self.host, 0))
            log_to_logfile_and_console(
                f"Данный порт занят, системой выдан свободный порт: {self.socket.getsockname()[1]}")

    def listen(self) -> None:
        """ Начало прослушивания порта. """
        try:
            self.socket.listen(1)
        except OSError as e:
            log_to_logfile_and_console(e)

    def wait_client(self) -> ConnectedClient:
        """ После подключения клиента метод возвращает новый объект типа ConnectedClient, принимающий в конструктор
        сокет соединения с клиентом и его данные подключения. """
        log_to_logfile_and_console(f"Ожидание клиента...")
        client_socket, client_address = self.socket.accept()
        log_to_logfile_and_console(f"\n \033[34m\033[3m !Подключение клиента {client_address}\033[0m\n")
        self.connected_clients.append(client := ConnectedClient(client_socket, client_address))
        return client

    def stop(self) -> None:
        """ Отключение серверного сокета. """
        self.socket.close()
        log_to_logfile_and_console("Остановка сервера.")


if __name__ == "__main__":
    server = Server()
    try:
        server.bind_socket(validate_port(input("Введите номер порта (по умолчанию 9090): ")))
        server.listen()
        while True:
            client = server.wait_client()
            client_thread = Thread(target=client.start)
            client_thread.start()
    except Exception as exc:
        print(f"Где-то что-то пошло не так. Ну и ладно. Не грустите, вот вам <3. {exc.args}")
    finally:
        server.stop()
