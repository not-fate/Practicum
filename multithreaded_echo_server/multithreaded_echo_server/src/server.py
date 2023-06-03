import logging
import socket as _socket
from threading import Thread
from multithreaded_echo_server.src.modules.connected_client import ConnectedClient
from utilities import log_to_logfile_and_console, validate_port

logging.basicConfig(format="%(asctime)s - %(message)s",
                    level=logging.INFO, filename="logs/server.log",
                    filemode="w")


class Server:
    """ Класс, представляющий эхо-сервер.

    @port - номер порта.
    @connected_clients - список подключенных к серверу клиентов
    (необходимо для реализаций п.п. 3,4 в лаб. "practicum4sem").
    @socket - сокет для последующего соединения с клиентами.
    @recv_buffer - размер буфера для записи читаемых данных.

    """

    def __init__(self, port: int, recv_buffer: int = 1024):
        self.port: int = 0
        self.host: str = "127.0.0.1"
        self.connected_clients: list[ConnectedClient] = []
        self.socket: _socket = _socket.socket()
        self.recv_buffer = recv_buffer
        self.bind_socket(port)
        log_to_logfile_and_console(f"Сервер запущен.")

    def bind_socket(self, port: int) -> None:
        """ [Реализация п.п. 4, 6 ~echo-server].
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

    def wait_client(self) -> ConnectedClient:
        """ После подключения клиента метод возвращает новый объект типа ConnectedClient, принимающий в конструктор
        сокет соединения с клиентом и его данные подключения. """
        client_socket, client_address = self.socket.accept()
        log_to_logfile_and_console(f"\n\033[34m\033[3m-> Подключение клиента {client_address}\033[0m.\n")
        self.connected_clients.append(client := self.create_client(client_socket, client_address))
        return client

    def create_client(self, client_socket: _socket, client_address: str) -> ConnectedClient:
        """ Создание объекта подключенного объекта. """
        return ConnectedClient(client_socket, client_address, self.recv_buffer)

    def stop(self) -> None:
        """ Отключение серверного сокета. """
        self.socket.close()
        log_to_logfile_and_console("Остановка сервера.")

    def start(self) -> None:
        """ [ Реализация п.п. 4.]
        Для реализации управляющего потока необходимо запускать сервер в отдельном потоке. """
        Thread(target=self.start_listen, name="server_thread").start()

    def start_listen(self):
        try:
            self.socket.listen()
            log_to_logfile_and_console("Сервер готов к работе. Ожидание клиентов...")
            while True:
                connected_client = self.wait_client()
                # -- [ п.п. 2. ~multithreaded-echo-server]
                Thread(target=connected_client.start,
                       name=str((connected_client.host,
                                 connected_client.port)),
                       daemon=True).start()
        except Exception as exc:
            print(f"Ошибка: {exc.args}")
        finally:
            self.stop()


if __name__ == "__main__":
    port: int = validate_port(input("Введите номер порта для установки соединения (по "
                                    "умолчанию локально): "))
    Server(port).start()
