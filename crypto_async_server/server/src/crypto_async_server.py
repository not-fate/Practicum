import asyncio
from typing import NoReturn
from server.src.modules.crypto_async_stream import CryptoStream


class CryptoServer:
    def __init__(self, p: int, g: int):
        self.port: int = 0
        self.recv_buffer_size = 1024
        self.p, self.g = p, g
        print(f"Сервер запущен.")

    async def handle(self, reader, writer) -> NoReturn:
        print(f"...подключение клиента.")
        crypto = CryptoStream(self.p, self.g, reader, writer)
        await crypto.key_exchange(type="server")
        print(f"Стороны обменялись ключами. Секретный общий ключ: {crypto.secret_key}")
        while True:
            message = await crypto.read(self.recv_buffer_size)
            if not message:
                print(f"...разрыв соединения с клиентом.")
                break
            print(f"приняты данные от клиента: {message.decode()}...")
            await crypto.write(message)
            print(f"...отправлены данные клиенту...")
        writer.close()

    async def start(self) -> NoReturn:
        try:
            server = await asyncio.start_server(self.handle, 'localhost', 9090)
            print("Сервер готов к работе. Ожидание клиентов...")
            await server.serve_forever()
        except Exception as exc:
            print(f"Ошибка: {exc.args}")


try:
    asyncio.run(CryptoServer(113, 68).start())
except KeyboardInterrupt:
    # Задолбал этот ваш кейборд интеррапт...
    pass
