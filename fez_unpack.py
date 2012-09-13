#!/usr/bin/env python

import os
from binstream import BinaryReader


def unpack(src, dest):
    with open(src, 'rb') as in_file:
        reader = BinaryReader(in_file.read())
        capacity = reader.read(int)
        for _ in range(capacity):
            filename = reader.read(str)
            filesize = reader.read(int)
            filedata = reader.pull(filesize)
            print '"%s" : %d' % (filename, filesize)
            filename = os.path.join(dest, filename) + '.xnb'
            filedir, _, _ = filename.rpartition('\\')
            if filedir and not os.path.exists(filedir):
                os.makedirs(filedir)
            with open(filename, 'wb') as out_file:
                out_file.write(filedata)


def main():
    unpack('Essentials.pak', 'out_e')
    unpack('Other.pak', 'out_o')


if __name__ == '__main__':
    main()
