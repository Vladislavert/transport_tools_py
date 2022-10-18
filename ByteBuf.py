import struct

class ByteBuf:
    def __init__(self) -> None:
        self.buffer = bytearray()
        self.offset = 0
    
    def reset(self) -> None:
        self.buffer.clear()
        self.offset = 0

    def get_size(self):
        return (len(self.buffer))
    
    def writeDouble(self, value) -> None:
        self.buffer += bytearray(struct.pack("d", value))

    def writeDoubleList(self, value) -> None:
        for i in range(len(value)):
            self.buffer += bytearray(struct.pack("d", value[i]))
    
    def writeInt(self, value) -> None:
        self.buffer += bytearray(struct.pack("i", value))

    def writeIntList(self, value) -> None:
        for i in range(len(value)):
            self.buffer += bytearray(struct.pack("i", value))
    
    def writeInt16(self, value) -> None:
        self.buffer += bytearray(struct.pack("h", value))

    def writeInt16List(self, value) -> None:
        for i in range(len(value)):
            self.buffer += bytearray(struct.pack("h", value))
    
    def writeBool(self, value) -> None:
        self.buffer += bytearray(struct.pack("?", value))

    def writeBoolList(self, value) -> None:
        for i in range(len(value)):
            self.buffer += bytearray(struct.pack("?", value))
    
    def writeChar(self, value) -> None:
        s = bytes(value, 'ascii') 
        self.buffer += bytearray(s)
        
    def writeByte(self, value) -> None:
        self.buffer += bytearray(struct.pack("B", value))
    
    def writeBytes(self, value) -> None:
        self.buffer += bytearray(struct.pack('%sB' % len(value), *value))
    
    def writeString(self, value) -> None:
        s = bytes(value, 'utf-8')
        self.buffer += bytearray(s)
    
    def readBool(self):
        val = struct.unpack_from("?", self.buffer, offset=self.offset)[0]
        self.offset += 1
        return val
    
    def readInt(self):
        val = struct.unpack_from("i", self.buffer, offset=self.offset)[0]
        self.offset += 4
        return val
    
    def readInt16(self):
        val = struct.unpack_from("h", self.buffer, offset=self.offset)[0]
        self.offset += 2
        return val
    
    def readByte(self):
        val = struct.unpack_from("B", self.buffer, offset=self.offset)[0]
        self.offset += 1
        return val

    def readBytes(self):
        val = self.buffer[self.offset:self.offset+len(self.buffer)]
        self.offset += len(self.buffer)
        return val
    
    def readDouble(self):
        val = struct.unpack_from("d", self.buffer, offset=self.offset)[0]
        self.offset += 8
        return val

    def readString(self, size):
        val = self.buffer[self.offset:self.offset+size].decode("utf-8")
        self.offset += size
        return val
    
