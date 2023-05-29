import logging
from helper import log_to_logfile_and_console


class ConnectedClient:
    def __init__(self, socket, address):
        self.socket = socket
        self.host, self.port = address
        logging.basicConfig(format="%(asctime)s - %(message)s",
                            level=logging.INFO, filename="logs/server_log.log",
                            filemode="w")

    def receive_message(self) -> bytes:
        log_to_logfile_and_console(f"\n...ожидание данных от {self.host, self.port}...")
        if not (message := self.socket.recv(1024)):
            return b''
        log_to_logfile_and_console(f"принято {len(message)} байт от {self.host, self.port}.")
        return message

    def send_message(self, message: bytes) -> None:
        self.socket.send(message)
        log_to_logfile_and_console(f"отправка данных [{message}] клиенту {self.host, self.port}...")

    def start(self) -> None:
        while True:
            message: bytes = self.receive_message()
            if not message:
                log_to_logfile_and_console(f"\033[34m\033[3m Отключение клиента {self.host, self.port}.\033[0m\n")
                break
            self.send_message(message)



