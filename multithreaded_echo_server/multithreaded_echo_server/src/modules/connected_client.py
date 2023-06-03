from utilities import log_to_logfile_and_console


class ConnectedClient:
    """ Объект, представляющий подключение определенного клиента.

    @socket - сокет подключения.
    @host, @port - адресные данные подключенного клиента.
    @recv_buffer - размер буфера для записи читаемых данных.

    """

    def __init__(self, socket, address, recv_size):
        self.socket = socket
        self.host, self.port = address
        self.recv_size = recv_size

    def receive_message(self) -> bytes:
        """ Принятие данных от клиента. """
        log_to_logfile_and_console(f"...ожидание данных от {self.host, self.port}...")
        message = self.socket.recv(self.recv_size)
        log_to_logfile_and_console(f"принято {len(message)} байт от {self.host, self.port}.")
        return message

    def send_message(self, message: bytes) -> None:
        """ Отправка данных клиенту. """
        self.socket.send(message)
        log_to_logfile_and_console(f"отправка данных клиенту {self.host, self.port}...")

    def start(self) -> None:
        """ Вся логика обработки клиента находится в этом методе. """
        try:
            while True:
                message: bytes = self.receive_message()
                # -- [ п.п. 2 ~echo-server]
                if not message or message == 'exit':
                    break
                self.send_message(message)
        except Exception as e:
            log_to_logfile_and_console(f"\033[34m\033[3mКод ошибки: [{e}]")
        finally:
            self.stop()

    def stop(self):
        log_to_logfile_and_console(f"\033[34m\033[3m-> Соединение с клиентом {self.host, self.port} разорвано. "
                                   f"\033[0m\n")
        self.socket.close()
