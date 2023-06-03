import os
from mmap import *

from src.modules.http_header_creater import HTTPHeader
from utilities import *

from src.utilities import validate_filetype, parse_http_query, log_to_logfile_and_console


class ConnectedClient:
    """ Объект, представляющий подключение клиента.

    @socket - сокет подключения.
    @host, @port - адресные данные подключенного клиента.
    @recv_buffer - размер буфера для записи читаемых данных.

    """

    def __init__(self, socket, address, work_directory, recv_buffer):
        self.socket = socket
        self.host, self.port = address
        self.recv_buffer = recv_buffer
        self.work_directory = work_directory

    def receive_message(self) -> bytes:
        """ Принятие данных от клиента. """
        log_to_logfile_and_console(f"...ожидание данных от {self.host, self.port}...")
        message = self.socket.recv(self.recv_buffer)
        if not message:
            return message
        log_to_logfile_and_console(f"принято {len(message)} байт от {self.host, self.port}.")
        return message

    def send_message(self, message: bytes) -> None:
        """ Отправка данных клиенту. """
        self.socket.send(message)
        log_to_logfile_and_console(f"отправка данных клиенту {self.host, self.port}...")

    def start(self) -> None:
        """
        Логика обработки клиента.
        """
        try:
            while True:
                message: bytes = self.receive_message()
                if not message:
                    break
                type, url, http_headers = parse_http_query(message.decode())
                if url == "/":
                    url = "/index.html"
                content_path = self.work_directory + url
                if not os.path.exists(content_path):
                    # -- [ п.п. 3. ]
                    # Если файл не найден, сервер передает в сокет специальный код ошибки - 404. /
                    self.send_message(HTTPHeader(type, '', "404 NOTFOUND", b"").get_response())
                elif not validate_filetype(content_path):
                    # -- [ п.п. 6 ]
                    # Клиент может запрашивать только определенные типы файлов (.html, .pdf, и .png в данном случае).
                    # При запросе неразрешенного типа сервер отправляет клиенту код ошибки 403.
                    self.send_message(HTTPHeader(type, '', "403 FORBIDDEN", b"").get_response())
                else:
                    # -- [ п.п. 8 ]
                    # Реализована поддержка абсолютно любых типов файлов.
                    with open(content_path, 'rb') as f:
                        # Дополнительная реализация п.п. 4:
                        # mmap позволяет нескольким потокам обращаться к одним и тем же файлам.
                        with mmap(f.fileno(), length=0, access=ACCESS_READ) as fr:
                            content = fr.read()
                    self.send_message(HTTPHeader(type, url, "200 OK", content).get_response() + content)
                if http_headers['Connection'] != 'keep-alive':
                    # -- [ п.п. 7. ]
                    # Реализация HTTP persistent connection. /
                    break
        except Exception as e:
            log_to_logfile_and_console(f"Клиент: {self.host, self.port} -> Код ошибки: [{e}]")
        finally:
            self.stop()

    def stop(self):
        log_to_logfile_and_console(f"\033[34m\033[3m Соединение с клиентом {self.host, self.port} разорвано. "
                                   f"\033[0m\n")
        self.socket.close()
