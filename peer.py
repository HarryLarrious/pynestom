import socket
import struct
from enum import Enum

from packet.packet import Packet


class State(Enum):
    HANDSHAKING = 0
    STATUS = 1
    LOGIN = 2
    CONFIGURATION = 3
    PLAY = 4


class Peer:
    def __init__(self, sock: socket.socket, addr):
        self.sock: socket.socket = sock
        self.addr: str = addr
        self.state: State = State.HANDSHAKING
        self.username: str = ""
        self.sent_uuid: bytes = b"\x00" * 16
        self.uuid: bytes = b"\x00" * 16
        self.bytecount: int = 0

    def write(self, b: bytes):
        print("send", b)
        self.sock.sendall(b)

    def send(self, packet: Packet):
        self.write(Packet(0).write_varint(len(packet.bytes) + 1).bytes)
        self.write(struct.pack("B", packet.packet_id))
        self.write(packet.bytes)

    def read(self, count: int) -> bytes:
        if count == 0:
            return b""
        bytes = self.sock.recv(count)
        if not bytes:
            raise ConnectionError("connection closed")
        self.bytecount += len(bytes)
        return bytes

    def read_varint(self) -> int:
        shift = 0
        value = 0
        while True:
            byte = self.read(1)[0]
            value |= (byte & 0x7F) << shift
            shift += 7
            if byte & 0x80 == 0:
                break
        return value

    def read_str(self) -> str:
        length = self.read_varint()
        bytes = self.read(length)
        return bytes.decode("utf-8")
