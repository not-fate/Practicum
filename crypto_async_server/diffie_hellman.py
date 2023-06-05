import struct

import random
from typing import NoReturn


class DiffieHellman:
    def __init__(self, p: int, g: int):
        self.p = p
        self.g = g
        self.private_key = self.get_private_key()
        self.public_key = self.get_public_key()
        self.secret_key: int | None = None

    @staticmethod
    def get_prime_number(start: int, end: int) -> int:
        return random.choice([x for x in range(start, end) if all(x % y != 0 for y in range(2, int(x ** 0.5) + 1))])

    def get_private_key(self) -> int:
        return random.randint(2, self.p - 1)

    def get_public_key(self) -> int:
        return (self.g ** self.private_key) % self.p

    def get_secret_key(self, outer_public_key) -> int:
        return (outer_public_key ** self.private_key) % self.p

    def set_secret_key(self, outer_public_key) -> NoReturn:
        outer_public_key = struct.unpack("i", outer_public_key)[0]
        self.secret_key = self.get_secret_key(outer_public_key)

    def get_public_key_bin(self) -> bytes:
        return struct.pack("i", self.public_key)

    def encrypt(self, message: bytes) -> bytes:
        return bytes([_ ^ self.secret_key for _ in message])

    def decrypt(self, message: bytes) -> bytes:
        return bytes([_ ^ self.secret_key for _ in message])
