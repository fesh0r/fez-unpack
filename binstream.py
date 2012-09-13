"""
.NET BinaryStream reader
"""

import struct


class BinaryReader(object):
    _types = {
        int: struct.Struct('<i'),
        float: struct.Struct('<d'),
        bool: struct.Struct('<?'),
    }
    _formats = {
        int: 'i',
        float: 'd',
        bool: '?',
    }
    _sizes = {
        int: 4,
        float: 8,
        bool: 1,
    }

    def __init__(self, serial):
        self.stream = serial
        self.index = 0

    def read(self, type_):
        try:
            value = self._types[type_].unpack_from(self.stream, self.index)[0]
            self.index += self._sizes[type_]
        except KeyError:
            if type_ == str:
                size = self.read_7bit_int()
                value = self.stream[self.index:self.index + size]
                self.index += size
            elif hasattr(type_, 'load'):
                value = type_.load(self.read(str))
            else:
                raise
        return value

    def next(self, count):
        return self.stream[self.index:self.index + count]

    def pull(self, count):
        value = self.stream[self.index:self.index + count]
        self.index += count
        return value

    def remainder(self):
        value = self.stream[self.index:]
        self.index = len(self.stream)
        return value

    def peek(self, type_):
        index = self.index
        value = self.read(type_)
        self.index = index
        return value

    def peek_list(self, type_):
        index = self.index
        value = self.read_list(type_)
        self.index = index
        return value

    def peek_dict(self, k, v):
        index = self.index
        value = self.read_dict(k, v)
        self.index = index
        return value

    def read_double(self):
        return self.read(float)

    def read_float(self):
        return struct.unpack('f', self.pull(4))[0]

    def read_7bit_int(self):
        value = 0
        shift = 0
        while True:
            val = ord(self.pull(1))
            value |= (val & 0x7F) << shift
            if val & 128 == 0:
                break
            shift += 7
        return value

    def read_list(self, type_):
        size = self.read(int)
        if type_ in self._formats:
            value = list(struct.unpack_from("<" + (self._formats[type_] * size), self.stream, self.index))
            self.index += (size * self._sizes[type_])
        elif type_ == bytes:
            value = [self.read(str) for _ in range(size)]
        elif hasattr(type_, 'load'):
            value = [type_.load(self.read(str)) for _ in range(size)]
        else:
            raise TypeError
        return value

    def read_dict(self, k, v):
        size = self.read(int)
        out_dict = {}
        for _ in range(size):
            key = self.read(k)
            value = self.read(v)
            out_dict[key] = value
        return out_dict
