import _socket
import os
from getpass import getpass

from utilities import get_full_path


class Client:

    def __init__(self, host, port, directory):
        self.socket = _socket.socket(proto=_socket.IPPROTO_TCP)
        self.in_connect: bool = False
        self.server_port: int = port
        self.server_address: str = host
        self.work_directory = directory

    @staticmethod
    def get_request(command, content=None):
        if content:
            return f"{command}\n{len(content)}\n".encode() + content
        else:
            return f"{command}\n".encode()

    def connection_to_server(self, address: str, port: int) -> None:
        try:
            self.socket.connect((self.server_address, self.server_port))
            print(f"\n\033[34m-> Соединение с сервером {(address, port)} установлено.\033[0m\n")
            self.server_address, self.server_port, self.in_connect = address, port, True
        except OSError as e:
            print(f"Соединение с сервером установить не удалось. Проверьте данные для "
                  f"подключения к серверу.\n {e}")

    def send_message(self, message: bytes) -> None:
        self.socket.send(message)
        print('Отправка запроса на сервер...')

    def receive_message(self) -> bytes:
        message = self.socket.recv(1024)
        print(f"Прием данных от сервера...")
        return message

    def stop(self) -> None:
        self.socket.close()
        print("Закрытие соединения.")

    def start(self):
        try:
            print(f"Клиент готов к работе.\n"
                  f"Адрес сервера, к которому произведено подключение: {self.server_address, self.server_port}.\n"
                  f"Клиентская директория: {os.path.abspath(self.work_directory)}\n")

            self.connection_to_server("localhost", 9090)

            if self.in_connect:
                while True:
                    login = input("Введите логин: ")
                    password = getpass(prompt='Введите пароль: ')
                    self.send_message(f"{login}:{password}".encode())
                    auth_rez = self.receive_message().decode()
                    print("Сервер: " + auth_rez)
                    if auth_rez.startswith("OK"):
                        break
                while message := input("Введите команду: "):
                    request = message.split(" ")
                    if request[0] == "upload":
                        full_path = get_full_path(self.work_directory, request[1])
                        if not os.path.exists(full_path):
                            print('Файла не существует')
                        else:
                            with open(full_path, 'rb') as f:
                                content = f.read()
                            destination_folder = request[2] if len(request) > 2 else '/'
                            path = os.path.join(destination_folder, os.path.basename(request[1]))
                            self.send_message(Client.get_request("upload " + path, content))
                            print("Сервер: " + self.receive_message().decode())

                    elif request[0] == 'download':
                        self.send_message(Client.get_request(message))
                        resp = self.receive_message()
                        header, content = resp.split(b"\n", 1)
                        header = header.decode()
                        print("Сервер: " + header)

                        status, info = header.split(" ", 1)
                        if status == "OK":
                            content_size, content = content.split(b"\n", 1)
                            content_size = int(content_size.decode())
                            while len(content) < content_size:
                                content += self.receive_message()

                            full_path = get_full_path(self.work_directory, request[1])
                            file = os.path.join(self.work_directory, os.path.basename(full_path))
                            with open(file, 'wb') as f:
                                f.write(content)
                            print(f"Файл {request[1]} сохранен.")

                    elif request[0] == 'exit':
                        break
                    else:
                        self.send_message(Client.get_request(message))
                        print("Сервер: " + self.receive_message().decode())
        except Exception as exc:
            print(f"Ошибка: {exc.args}")
        finally:
            self.stop()


try:
    Client("127.0.0.1", 9090, "/Users/notefate/PycharmProjects/midterm/ftp-server/ftp-client/documents").start()
except KeyboardInterrupt:
    pass


