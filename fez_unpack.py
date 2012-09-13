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
            filename = os.path.join(dest, filename) + '.xnb'
            filedir, _, _ = filename.rpartition('\\')
            if filedir:
                filedir = os.path.normpath(filedir)
                if not os.path.isdir(filedir):
                    os.makedirs(filedir)
            with open(filename, 'wb') as out_file:
                out_file.write(filedata)


def main():
    if len(sys.argv) == 3:
        unpack(sys.argv[1], sys.argv[2])
    else:
        print 'fez_unpack.py in.pak out_dir'


if __name__ == '__main__':
    main()
