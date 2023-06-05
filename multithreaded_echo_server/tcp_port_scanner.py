import os
import socket
import threading
import time


class TCPPortScanner:
    def __init__(self, host: str):
        self.__host = host
        self.open_ports = []
        self.__lock = threading.Lock()
        self.__count_check_ports = 0

    def scan_port(self, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
        sock.settimeout(1)
        attempt = sock.connect_ex((self.__host, port))
        if attempt == 0:
            with self.__lock:
                self.open_ports.append(port)
        sock.close()

    def __scanning(self, port_range_start, port_range_end: int) -> None:
        for _ in range(port_range_start, port_range_end + 1):
            self.scan_port(_)
            with self.__lock:
                self.__count_check_ports += 1

    def process(self, thread_count: int) -> list[int]:
        self.__count_check_ports = 0
        thread_count = thread_count
        max_port = 65535
        scanner_threads: list[threading.Thread] = []

        for _ in range(0, thread_count + 1):
            start_port = (max_port + thread_count - 1) // thread_count * _ + 1
            end_port = (max_port + thread_count - 1) // thread_count * (_ + 1)
            if end_port > max_port:
                end_port = max_port
            thread = threading.Thread(target=self.__scanning, daemon=True, args=(start_port, end_port))
            scanner_threads.append(thread)
            thread.start()

        while True:

            # запускать скрипт в Terminal (не в Run), если не включена поддержка терминала.
            # Для виндуса поменять команду на 'cls'.

            print(f"Процесс сканирования ресурса {self.__host}: {self.__count_check_ports / max_port * 100:.2f}%")
            if self.__count_check_ports >= max_port:
                print("Процесс сканирования завершен.")
                break
            time.sleep(0.1)
            os.system('clear')

        for scanner_process in scanner_threads:
            scanner_process.join()
        return sorted(self.open_ports)


scanner = TCPPortScanner("127.0.0.1")
res = scanner.process(500)
print(f'\nПрослушиваемые порты: {res}')
