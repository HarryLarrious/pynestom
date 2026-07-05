from io import UnsupportedOperation
from typing import List, Dict
import struct

class NbtElement:
    TAG = None
    def encode_tagless(self) -> bytes:
        raise UnsupportedOperation("unimplemented")
    def encode(self) -> bytes:
        return struct.pack("B", self.TAG) + self.encode_tagless()

class NbtByte(NbtElement):
    TAG = 1
    def __init__(self, v : int):
        self.v = v
    def encode_tagless(self) -> bytes:
        return struct.pack("B", self.v)

class NbtShort(NbtElement):
    TAG = 2
    def __init__(self, v : int):
        self.v = v
    def encode_tagless(self) -> bytes:
        return struct.pack(">h", self.v)

class NbtInt(NbtElement):
    TAG = 3
    def __init__(self, v : int):
        self.v = v
    def encode_tagless(self) -> bytes:
        return struct.pack(">i", self.v)

class NbtLong(NbtElement):
    TAG = 4
    def __init__(self, v : int):
        self.v = v
    def encode_tagless(self) -> bytes:
        return struct.pack(">l", self.v)

class NbtFloat(NbtElement):
    TAG = 5
    def __init__(self, v : float):
        self.v = v
    def encode_tagless(self) -> bytes:
        return struct.pack(">f", self.v)

class NbtDouble(NbtElement):
    TAG = 6
    def __init__(self, v : float):
        self.v = v
    def encode_tagless(self) -> bytes:
        return struct.pack(">d", self.v)

# class NbtBArray(NbtElement):
#     TAG = 7
#     def __init__(self, v : List[int]):
#         self.v = v

class NbtString(NbtElement):
    TAG = 8
    def __init__(self, v : str):
        self.v = v
    def encode_tagless(self) -> bytes:
        s = self.v.encode('utf-8')
        return struct.pack(">H", len(s)) + s

class NbtList(NbtElement):
    TAG = 9
    def __init__(self, v : List[NbtElement]):
        self.v = v
    def encode_tagless(self) -> bytes:
        count     = len(self.v)
        inner_tag = self.v[0].TAG if count > 0 else 0
        b = struct.pack("B", inner_tag) + struct.pack(">I", count)
        for e in self.v:
            b += e.encode_tagless()
        return b

class NbtCompound(NbtElement):
    TAG = 10
    def __init__(self, v : Dict[str, NbtElement]):
        self.v = v
    def encode_tagless(self) -> bytes:
        b = b''
        for k in self.v.keys():
            v = self.v[k]
            b += struct.pack("B", v.TAG)
            b += NbtString(k).encode_tagless()
            b += v.encode_tagless()
        return b + struct.pack("B", 0)

# class NbtIArray(NbtElement):
#     TAG = 11
#     def __init__(self, v : List[int]):
#         self.v = v

# class NbtLArray(NbtElement):
#     TAG = 12
#     def __init__(self, v : List[int]):
#         self.v = v
