import struct


class ByteBuf:
    def __init__(self) -> None:
        self.buffer = bytearray()
        self.offset = 0

    def reset(self) -> None:
        self.buffer.clear()
        self.offset = 0

    def get_size(self):
        return len(self.buffer)

    def write_double(self, value: float) -> None:
        self.buffer += bytearray(struct.pack("d", value))

    def write_double_list(self, value: list[float]) -> None:
        for val in value:
            self.buffer += bytearray(struct.pack("d", val))

    def write_int(self, value: int) -> None:
        self.buffer += bytearray(struct.pack("i", value))

    def write_int_list(self, value: list[int]) -> None:
        for val in value:
            self.buffer += bytearray(struct.pack("i", val))

    def write_int16(self, value: int) -> None:
        self.buffer += bytearray(struct.pack("h", value))

    def write_int16_list(self, value: list[int]) -> None:
        for val in value:
            self.buffer += bytearray(struct.pack("h", val))

    def write_bool(self, value: bool) -> None:
        self.buffer += bytearray(struct.pack("?", value))

    def write_bool_list(self, value: list[bool]) -> None:
        for val in value:
            self.buffer += bytearray(struct.pack("?", val))

    def write_char(self, value: str) -> None:
        s = bytes(value, 'ascii')
        self.buffer += bytearray(s)

    def write_byte(self, value: int) -> None:
        self.buffer += bytearray(struct.pack("B", value))

    def write_bytes(self, value: bytes) -> None:
        self.buffer += bytearray(struct.pack('%sB' % len(value), *value))

    def write_string(self, value: str) -> None:
        s = bytes(value, 'utf-8')
        self.buffer += bytearray(s)

    def read_bool(self) -> bool:
        val = struct.unpack_from("?", self.buffer, offset=self.offset)[0]
        self.offset += 1
        return val

    def read_int(self) -> int:
        val = struct.unpack_from("i", self.buffer, offset=self.offset)[0]
        self.offset += 4
        return val

    def read_int16(self) -> int:
        val = struct.unpack_from("h", self.buffer, offset=self.offset)[0]
        self.offset += 2
        return val

    def read_byte(self) -> int:
        val = struct.unpack_from("B", self.buffer, offset=self.offset)[0]
        self.offset += 1
        return val

    def read_bytes(self) -> bytes:
        val = self.buffer[self.offset:self.offset + len(self.buffer)]
        self.offset += len(self.buffer)
        return val

    def read_double(self) -> float:
        val = struct.unpack_from("d", self.buffer, offset=self.offset)[0]
        self.offset += 8
        return val

    def read_string(self, size: int, encoding="utf-8") -> str:
        val = self.buffer[self.offset:self.offset + size].decode(encoding)
        self.offset += size
        return val
