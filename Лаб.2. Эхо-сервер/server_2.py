import socket
import logging

logging.basicConfig(format="%(asctime)s - %(message)s",
                    level=logging.INFO, filename="server_log.log",
                    filemode="w")

logging.info('Запуск сервера')

sock = socket.socket()


def bind_socket(port: int, sock: socket) -> None:
    try:
        sock.bind(('', port))
        print(f"К сокету привязан порт: {sock.getsockname()}")
    except Exception:
        sock.bind(('', 0))
        print(f"Данный порт занят, системой выдан свободный порт: {sock.getsockname()[1]}")
        logging.info(f"Данный порт занят, системой выдан свободный порт: {sock.getsockname()[1]}")


port = int(port) if (port := input("Введите номер порта: ")).isdigit() and 1 < int(port) < 65535 else 9090
bind_socket(port, sock)

sock.listen(1)
logging.info(f"Сервер запущен.")

while True:
    conn, addr = sock.accept()
    logging.info(f"Подключение клиента {addr}")

    while True:

        logging.info("\n...прием данных от клиента...")
        data = conn.recv(1024)
        if not data:
            logging.info("Отключение клиента.")
            break
        logging.info(f"принято {len(data)} байт.")
        conn.send(data.upper())
        logging.info(f"отправка данных {data} клиенту...")

logging.info("Остановка сервера.")
conn.close()
