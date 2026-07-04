import struct
from typing import Self, Union

from nbt import NbtElement


class Packet:
    def __init__(self, packet_id: int):
        self.packet_id = packet_id
        self.bytes = b""

    def write(self, b: Union[int, bool, bytes]) -> Self:
        if isinstance(b, int):
            self.bytes += struct.pack("B", b)
        elif isinstance(b, bool):
            self.bytes += struct.pack("B", 1 if b else 0)
        elif isinstance(b, bytes):
            self.bytes += b
        else:
            raise ConnectionError(f"unknown bytes type: `{type(b)}`")
        return self

    def write_varint(self, value: int) -> Self:
        data = b""
        while True:
            byte = value & 0x7F
            value >>= 7
            if value != 0:
                data += struct.pack("B", byte | 0x80)
            else:
                data += struct.pack("B", byte)
                break
        self.write(data)
        return self

    def write_str(self, value: str) -> Self:
        encoded = value.encode("utf-8")
        self.write_varint(len(encoded))
        self.write(encoded)
        return self

    def write_nbt(self, nbt: NbtElement) -> Self:
        self.write(nbt.encode())
        return self
