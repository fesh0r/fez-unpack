#!/usr/bin/env python

"""
Extract FEZ .pak files
"""

import sys
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
            filename = os.path.join(dest, filename)
            filedir, _, _ = filename.rpartition('\\')
            if filedir:
                filedir = os.path.normpath(filedir)
                if not os.path.isdir(filedir):
                    os.makedirs(filedir)
            if filedata[:3] == b'XNB':
                extension = '.xnb'
            elif filedata[:4] == b'OggS':
                extension = '.ogg'
            elif filedata[:4] == b'XGSF' or filedata[:4] == b'FSGX':
                extension = '.xgs'
            elif filedata[:4] == b'SDBK' or filedata[:4] == b'KBDS':
                extension = '.xsb'
            elif filedata[:4] == b'WBND' or filedata[:4] == b'DNBW':
                extension = '.xwb'
            elif filedata[2:4] == b'\xff\xfe' or filedata[:2] == b'\xfe\xff':
                extension = '.fxo'
            else:
                extension = '.bin'
            suffix = ''
            if os.path.isfile(filename + suffix + extension):
                for i in range(0, 100):
                    suffix = '.%02d' % i
                    if not os.path.isfile(filename + suffix + extension):
                        break
            with open(filename + suffix + extension, 'wb') as out_file:
                out_file.write(filedata)


def main():
    if len(sys.argv) == 3:
        unpack(sys.argv[1], sys.argv[2])
    else:
        print 'fez_unpack.py in.pak out_dir'


if __name__ == '__main__':
    main()
