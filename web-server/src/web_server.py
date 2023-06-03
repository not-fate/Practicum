import socket as _socket
from _socket import IPPROTO_TCP
from threading import Thread

from src.config import *
from src.modules.web_connected_client import ConnectedClient
from utilities import *


class WebServer:
    """ Класс, представляющий веб-сервер.

    @port - номер порта.
    @recv_buffer - размер буфера.
    @directory - рабочая директория сервера (папка с контентом, который сервер отдает клиентам).

    """

    def __init__(self, port: int, recv_buffer: int, directory: str):
        self.port: int = 0
        self.host: str = "127.0.0.1"
        self.socket: _socket = _socket.socket(proto=IPPROTO_TCP)
        self.recv_buffer = recv_buffer
        self.directory = directory
        self.bind_socket(port)
        log_to_logfile_and_console(f"Сервер запущен.")

    def bind_socket(self, port: int) -> None:
        try:
            self.socket.bind((self.host, port))
            log_to_logfile_and_console(f"К сокету привязан порт: {self.socket.getsockname()}")
        except OSError:
            self.socket.bind((self.host, 0))
            log_to_logfile_and_console(
                f"Данный порт занят, системой выдан свободный порт: {self.socket.getsockname()[1]}")

    def wait_client(self) -> ConnectedClient:
        """ После подключения клиента метод возвращает новый объект типа ConnectedClient, принимающий в конструктор
        сокет соединения с клиентом и его данные подключения. """
        client_socket, client_address = self.socket.accept()
        log_to_logfile_and_console(f"\n\033[34m\033[3m !Подключение клиента {client_address}\033[0m\n")
        client = self.create_client(client_socket, client_address)
        return client

    def create_client(self, client_socket: _socket, client_address: str) -> ConnectedClient:
        """ Создание объекта подключенного клиента. """
        return ConnectedClient(client_socket, client_address, self.directory, self.recv_buffer)

    def stop(self) -> None:
        self.socket.close()
        log_to_logfile_and_console("Остановка сервера.")
        exit(0)

    def start_listen(self):
        try:
            self.socket.listen()
            log_to_logfile_and_console("Сервер готов к работе. Ожидание клиентов...")
            while True:
                client = self.wait_client()
                # [ п.п. 4]
                # Поток с daemon=True создается для того,
                # чтобы существование потоков-подключений не мешало завершению мейн-скрипта.
                Thread(target=client.start, name=str((client.host, client.port)), daemon=True).start()
        except Exception as e:
            log_to_logfile_and_console(f"{e.args}")
        finally:
            self.stop()


if __name__ == "__main__":
    WebServer(PORT, RECV_BUFFER, SERVER_DIRECTORY).start_listen()
