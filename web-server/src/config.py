""" [Реализация п.п. 2]
Конфигурационный файл позволяет задать порт, рабочую директорию и размер буфера у веб-сервера."""
import logging

logging.basicConfig(format="%(asctime)s - %(message)s",
                    level=logging.INFO, filename="logs/server.log",
                    filemode="w")

PORT = 8080
SERVER_DIRECTORY = "/Users/notefate/PycharmProjects/midterm/web-server/src/content"
RECV_BUFFER = 8192
