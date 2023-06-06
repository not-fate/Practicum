import _socket
import socket
from threading import Thread
from ftp_connected_client import *


class FTPServer:
    def __init__(self, port: int, directory: str, recv_buffer_size: int = 1024, max_user_diskspace=100):
        self.socket = socket.socket(proto=_socket.IPPROTO_TCP)
        self.host = '127.0.0.1'
        self.port = port
        self.recv_buffer_size = recv_buffer_size
        self.directory = directory
        self.logins = Authentication()
        self.max_user_diskspace = max_user_diskspace

    def wait_client(self) -> FTPConnectedClient:
        client_socket, client_address = self.socket.accept()
        print(f"\n\033[34m-> Подключение клиента {client_address}\033[0m\n")
        return self.create_client(client_socket, client_address)

    def create_client(self, client_socket: _socket, client_address: str) -> FTPConnectedClient:
        return FTPConnectedClient(client_socket, client_address, self.directory, self.recv_buffer_size, self.logins,
                                  self.max_user_diskspace)

    def stop(self) -> None:
        self.socket.close()

    def start(self) -> None:
        server_thread = Thread(target=self.start_listen, name="server_thread")
        server_thread.start()

    def start_listen(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            print(f"Сервер готов к работе. Адрес сервера: {self.socket.getsockname()}.\n"
                  f"Рабочая директория: {os.path.abspath(self.directory)}\n"
                  f"Размер клиентских директорий: {self.max_user_diskspace} байт.\n"
                  f"Ожидание клиентов...")
            while True:
                client = self.wait_client()
                client_thread = Thread(target=client.start, daemon=True)
                client_thread.start()
        except Exception as exc:
            print(f"Ошибка: {exc.args}")
        finally:
            self.stop()


try:
    FTPServer(9090, "/Users/notefate/PycharmProjects/midterm/ftp-server/ftp-server/user_storage", 32768).start()
except KeyboardInterrupt:
    pass
