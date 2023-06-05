import asyncio

from server.src.modules.crypto_async_stream import CryptoStream


class CryptoClient:
    def __init__(self, p, g):
        self.p, self.g = p, g

    async def tcp_echo_client(self, host, port):
        reader, writer = await asyncio.open_connection(host, port)
        crypto = CryptoStream(self.p, self.g, reader, writer)
        print(f"Обмен ключами шифрования...")
        await crypto.key_exchange(type="client")
        print(f"Стороны обменялись ключами. Секретный общий ключ: {crypto.secret_key}.")
        while True:
            message = input("Введите сообщение для отправки на сервер: ")
            if not message:
                break
            await crypto.write(message.encode())
            decrypted_message = await crypto.read(100)
            print(f"Сообщение от сервера: {decrypted_message.decode()}.")
        writer.close()
        await writer.wait_closed()


try:
    asyncio.run(CryptoClient(113, 68).tcp_echo_client('localhost', 9090))
except KeyboardInterrupt:
    pass
