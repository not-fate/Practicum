from asyncio import StreamReader, StreamWriter
from typing import NoReturn

from diffie_hellman import DiffieHellman


class CryptoStream(DiffieHellman):
    def __init__(self, p: int, g: int, reader: StreamReader, writer: StreamWriter):
        super().__init__(p, g)
        self.reader = reader
        self.writer = writer

    async def key_exchange(self, type="server") -> NoReturn:
        if type == "server":
            client_public_key = await self.reader.read(4)
            self.set_secret_key(client_public_key)
            self.writer.write(self.get_public_key_bin())
            await self.writer.drain()
        else:
            self.writer.write(self.get_public_key_bin())
            await self.writer.drain()
            server_public_key = await self.reader.read(4)
            self.set_secret_key(server_public_key)

    async def read(self, recv_buffer_size: int) -> bytes:
        data: bytes = await self.reader.read(recv_buffer_size)
        if not data:
            return data
        message: bytes = self.decrypt(data)
        return message

    async def write(self, message: bytes) -> NoReturn:
        message: bytes = self.encrypt(message)
        self.writer.write(message)
        await self.writer.drain()
