import socket
import logging


logging.basicConfig(format="%(asctime)s - %(message)s",
                    level=logging.INFO, filename="server_log.log",
                    filemode="w")


def bind_socket(port: int, sock: socket) -> None:
    try:
        sock.bind(('', port))
        print(f"К сокету привязан порт: {sock.getsockname()}")
    except Exception as e:
        logging.error(e)
        sock.bind(('', 0))
        print(f"Данный порт занят, системой выдан свободный порт: {sock.getsockname()[1]}")
        logging.info(f"Данный порт занят, системой выдан свободный порт: {sock.getsockname()[1]}")


def receive_message(conn: socket):
    while True:
        print("\n...прием данных от клиента...")
        logging.info("\n...прием данных от клиента...")
        data = conn.recv(1024)
        if not data:
            print("Отключение клиента.")
            logging.info("Отключение клиента.")
            break
        print(f"принято {len(data)} байт.")
        logging.info(f"принято {len(data)} байт.")
        return data


def send_message(data: bytes) -> None:
    conn.send(data)
    print(f"отправка данных {data} клиенту...")
    logging.info(f"отправка данных {data} клиенту...")


def create_connection(sock: socket) -> tuple[socket, tuple]:
    print(f"Ожидание клиентов...")
    conn, addr = sock.accept()
    print(f"Подключение клиента {addr}")
    logging.info(f"Подключение клиента {addr}")
    return conn, addr


if __name__ == "__main__":
    sock = socket.socket()
    try:
        bind_socket(
            (int(port) if (port := input("Введите номер порта (по умолчанию 9090): ")).isdigit() and 1 < int(
                port) < 65535 else 9090),
            sock)
        sock.listen(1)
        print(f"Сервер запущен.")
        logging.info(f"Сервер запущен.")
        while True:
            conn, addr = create_connection(sock)
            logging.info(f"Подключение клиента {addr}")
            send_message(receive_message(conn))
    except Exception:
        print("Где-то что-то пошло не так. Ну и ладно. Не грустите, вот вам <3.")
    finally:
        logging.info("Остановка сервера.")
        sock.close()
