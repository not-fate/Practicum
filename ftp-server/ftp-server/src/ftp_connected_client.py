from auth import Authentication
from utilities import *


class FTPConnectedClient:
    def __init__(self, socket, address,
                 work_directory_server,
                 recv_buffer_size,
                 logins: Authentication,
                 max_user_diskspace):
        self.socket = socket
        self.address = address
        self.recv_buffer_size = recv_buffer_size
        self.work_directory_server = work_directory_server
        self.work_directory_user = ""
        self.logins = logins
        self.max_user_diskspace = max_user_diskspace
        self.is_logged = False
        self.is_admin = False

    @staticmethod
    def get_response(status, message, content=None):
        if content:
            return f"{status} {message}\n{len(content)}\n".encode() + content
        else:
            return f"{status} {message}\n".encode()

    def receive_message(self) -> bytes:
        message = self.socket.recv(self.recv_buffer_size)
        return message

    def send_message(self, message: bytes) -> None:
        self.socket.send(message)

    def start(self):
        try:
            while True:
                message: str = self.receive_message().decode()
                if not message:
                    break
                login, password = message.split(':')
                authentication_result = self.logins.check_login(login, password)
                if authentication_result > 0:
                    self.is_admin = authentication_result == 2
                    self.work_directory_user = os.path.join(self.work_directory_server, login)
                    create_folder_if_not_exist(self.work_directory_user + "/")
                    self.send_message(FTPConnectedClient.get_response("OK", f"Добро пожаловать, {login}!"))
                    break
                self.send_message(FTPConnectedClient.get_response("ERROR", " некорректный логин или пароль."))

            while True:
                message: bytes = self.receive_message()
                if len(message) < 1:
                    self.send_message(FTPConnectedClient.get_response("ERROR", "клиент отключился."))
                    break
                header, content = message.split(b"\n", 1)
                header = header.decode().split(" ")
                command = header[0]

                # -- Да, вот такая вот у меня свиноматочка. Вопросы?

                if command == 'ls':
                    folder = header[1] if len(header) > 1 else "/"
                    full_path = get_full_path(self.work_directory_user, folder)
                    if not os.path.exists(full_path):
                        self.send_message(FTPConnectedClient.get_response("ERROR", "папка не найдена."))
                    else:
                        dir_list = '\n\t'.join(os.listdir(full_path))
                        self.send_message(FTPConnectedClient.get_response("OK", f"содержимое папки: \n\t" + dir_list))

                elif command == 'mkdir':
                    folder = header[1] if len(header) > 1 else "/"
                    full_path = get_full_path(self.work_directory_user, folder)
                    if os.path.exists(full_path):
                        self.send_message(FTPConnectedClient.get_response("ERROR", "папка уже существует."))
                        continue
                    os.mkdir(full_path)
                    self.send_message(FTPConnectedClient.get_response("OK", f"папка {folder} создана."))

                elif command == "rmdir":
                    folder = header[1] if len(header) > 1 else "/"
                    full_path = get_full_path(self.work_directory_user, folder)
                    if not os.path.exists(full_path):
                        self.send_message(FTPConnectedClient.get_response("ERROR", "такой папки не существует."))
                    if len(os.listdir(full_path)) != 0:
                        self.send_message(FTPConnectedClient.get_response("ERROR", "Нельзя удалить не пустую папку."))
                    else:
                        os.rmdir(full_path)
                        self.send_message(FTPConnectedClient.get_response("OK", f"папка {folder} удалена."))

                elif command == "rm":
                    file = header[1] if len(header) > 1 else "/"
                    full_path = get_full_path(self.work_directory_user, file)
                    if not os.path.exists(full_path):
                        self.send_message(FTPConnectedClient.get_response("ERROR", "файл не найден."))
                    else:
                        os.remove(full_path)
                        self.send_message(FTPConnectedClient.get_response("OK", f"файл {file} удален."))

                elif command == 'upload':
                    full_path = get_full_path(self.work_directory_user, header[1])
                    if not os.path.exists(os.path.dirname(full_path)):
                        self.send_message(FTPConnectedClient.get_response("ERROR", "папки не существует."))
                    content_size, content = content.split(b"\n", 1)
                    content_size = int(content_size.decode())
                    while len(content) < content_size:
                        content += self.receive_message()
                    curr_size = get_full_size_directory(self.work_directory_user)
                    if curr_size + content_size > self.max_user_diskspace:
                        free_space = self.max_user_diskspace - curr_size
                        self.send_message(FTPConnectedClient.get_response("ERROR", f"недостаточно места на диске "
                                                                                   f"(свободное пространство: {str(free_space)} байт.)"))
                        continue
                    with open(full_path, 'wb') as f:
                        f.write(content)
                    self.send_message(FTPConnectedClient.get_response("OK", "файл загружен на сервер."))

                elif command == "download":
                    path = header[1]
                    full_path = get_full_path(self.work_directory_user, path)
                    if not os.path.exists(full_path):
                        self.send_message(FTPConnectedClient.get_response("ERROR", "файла не существует."))
                    else:
                        with open(full_path, 'rb') as f:
                            content = f.read()
                        self.send_message(FTPConnectedClient.get_response("OK", "файл загружен из сервера.", content))

                elif command == "create_user":
                    # Только администратор может создавать пользователей.
                    if not self.is_admin:
                        self.send_message(FTPConnectedClient.get_response("ERROR",
                                                                          "только администратор может создавать "
                                                                          "учетные записи."))
                        continue
                    new_login = header[1] if len(header) > 1 else ""
                    new_password = header[2] if len(header) > 2 else ""
                    if len(new_login) == 0:
                        self.send_message(FTPConnectedClient.get_response("ERROR", "логин не может быть пустым."))
                        continue
                    if not self.logins.add_user(new_login, new_password):
                        self.send_message(FTPConnectedClient.get_response("ERROR", f"{new_login} уже существует."))
                        continue
                    self.send_message(FTPConnectedClient.get_response("OK", f"пользователь {new_login} создан."))

                else:
                    self.send_message(FTPConnectedClient.get_response("ERROR", "неизвестная команда."))
                    continue
        except (Exception,) as e:
            print(f"Ошибка: {e}")
        finally:
            print(f"\n\033[31m-> Закрытие соединения с {self.address}\033[0m\n")
            self.socket.close()
