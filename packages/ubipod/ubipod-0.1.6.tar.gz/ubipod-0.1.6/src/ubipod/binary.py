import struct
from types import TracebackType
from typing import Any, BinaryIO, Protocol, Type, TypeVar

from .typing import mat33, vec2, vec2i32, vec3


class BinaryReadable(Protocol):
    def read(self, read: Any, *args: Any, **kwargs: Any): ...


class BinaryReader:
    T = TypeVar("T", bound=BinaryReadable)

    def __init__(self, file: BinaryIO, encoding: str = "cp1252") -> None:
        self.file = file
        self.encoding = encoding

    def __enter__(self) -> "BinaryReader":
        return self

    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        self.file.close()

    def bytes(self, count: int) -> bytes:
        result = bytearray(count)
        if self.file.readinto(result) != count:  # type: ignore
            raise OSError("Could not read complete buffer.")
        return result

    def any(self, t: Type[T], *args: Any, **kwargs: Any) -> T:
        value = t()
        value.read(self, *args, **kwargs)
        return value

    def b32(self) -> bool:
        return bool(self.i32())

    def f(self) -> float:
        return self.i32() / (1 << 16)  # fixed point 16x16

    def i8(self) -> int:
        return struct.unpack("<b", self.bytes(1))[0]

    def i16(self) -> int:
        return struct.unpack("<h", self.bytes(2))[0]

    def i32(self) -> int:
        return struct.unpack("<i", self.bytes(4))[0]

    def mat33(self) -> mat33:
        return self.f(), self.f(), self.f(), self.f(), self.f(), self.f(), self.f(), self.f(), self.f()

    def str(self) -> str:
        return bytes((c ^ ~i) & 0xFF for i, c in enumerate(self.bytes(self.u8()))).decode(self.encoding)

    def strbytes(self, count: int) -> 'str':
        return self.bytes(count).decode(self.encoding).rstrip('\x00')

    def u8(self) -> int:
        return struct.unpack("<B", self.bytes(1))[0]

    def u16(self) -> int:
        return struct.unpack("<H", self.bytes(2))[0]

    def u32(self) -> int:
        return struct.unpack("<I", self.bytes(4))[0]

    def vec2(self) -> vec2:
        return self.f(), self.f()

    def vec2i32(self) -> vec2i32:
        return self.i32(), self.i32()

    def vec3(self) -> vec3:
        return self.f(), self.f(), self.f()


class BinaryWritable(Protocol):
    def write(self, write: Any, *args: Any, **kwargs: Any): ...


class BinaryWriter:
    def __init__(self, file: BinaryIO, encoding: str = "cp1252") -> None:
        self.file = file
        self.encoding = encoding

    def __enter__(self) -> "BinaryWriter":
        return self

    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        self.file.close()

    def bytes(self, value: bytes) -> None:
        self.file.write(value)

    def any(self, value: BinaryWritable, *args: Any, **kwargs: Any) -> None:
        value.write(self, *args, **kwargs)

    def b32(self, value: bool) -> None:
        self.i32(value)

    def f(self, value: float) -> None:
        self.i32(int(value * (1 << 16)))  # fixed point 16x16

    def i8(self, value: int) -> None:
        self.bytes(struct.pack("<b", value))

    def i16(self, value: int) -> None:
        self.bytes(struct.pack("<h", value))

    def i32(self, value: int) -> None:
        self.bytes(struct.pack("<i", value))

    def mat33(self, value: mat33) -> None:
        self.f(value[0])
        self.f(value[1])
        self.f(value[2])
        self.f(value[3])
        self.f(value[4])
        self.f(value[5])
        self.f(value[6])
        self.f(value[7])
        self.f(value[8])

    def str(self, value: str) -> None:
        self.u8(len(value))
        self.bytes(bytes((c ^ ~i) & 0xFF for i, c in enumerate(value.encode(self.encoding))))

    def strbytes(self, value: 'str', count: int) -> None:
        bytes = bytearray(count)
        bytes[:len(value)] = value.encode(self.encoding)
        self.bytes(bytes)

    def u8(self, value: int) -> None:
        self.bytes(struct.pack("<B", value))

    def u16(self, value: int) -> None:
        self.bytes(struct.pack("<H", value))

    def u32(self, value: int) -> None:
        self.bytes(struct.pack("<I", value))

    def vec2(self, value: vec2) -> None:
        self.f(value[0])
        self.f(value[1])

    def vec2i32(self, value: vec2i32) -> None:
        self.i32(value[0])
        self.i32(value[1])

    def vec3(self, value: vec3) -> None:
        self.f(value[0])
        self.f(value[1])
        self.f(value[2])
