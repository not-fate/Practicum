import socket
import logging

logging.basicConfig(format="%(asctime)s - %(message)s",
                    level=logging.INFO, filename="client_log.log",
                    filemode="w")


def create_connection(sock: socket) -> bool:
    port = int(port) if (port := input("Введите номер порта (по умолчанию 9090): ")).isdigit() and 1 < int(port) < 65535 else 9090
    address = address if (address := input("Введите имя хоста для установки соединения (по умолчанию локально): ")) else '127.0.0.1'
    try:
        sock.connect((address, port))
        print(f"Соединение с сервером установлено {sock.getsockname()}.")
        logging.info(f"Соединение с сервером установлено {sock.getsockname()}.")
        return True
    except Exception as e:
        logging.error(e)
        print(f"Соединение с сервером установить не удалось. Проверьте данные для подключения к серверу.")
        logging.info(f"Соединение с сервером установить не удалось.")
        return False


def send_message(sock: socket) -> None:
    sock.send(input("Введите сообщение для отправки на сервер: ").encode())
    logging.info('Отправка сообщение на сервер.')


def receive_message(sock: socket) -> None:
    data = sock.recv(1024)
    logging.info(f"Прием данных от сервера {data}")
    print(f"Прием данных от сервера {data}")


if __name__ == "__main__":
    sock = socket.socket()
    try:
        if create_connection(sock):
            send_message(sock)
            receive_message(sock)
    except Exception:
        print("Где-то что-то пошло не так. Ну и ладно. Не грустите, вот вам <3.")
    finally:
        print("Закрытие сокета.")
        logging.info("Закрытие соединения.")
        sock.close()
