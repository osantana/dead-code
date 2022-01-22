#!/usr/bin/env python

import sys
import os
import re
import string
import mmap
import ntpath # BackupNOW! works only in Windows :)
from subprocess import *
from nstruct import *

# Utilities
DEBUG = False
def debug(*args):
    if not DEBUG:
        return
    print >>sys.stderr, "DEBUG:", ''.join([ str(x) for x in args ])


# NBF File format constants
NBF_START_SET = "SSET"
NBF_END_SET   = "ESET"
NBF_DIR_SIGN  = "DIRB"
NBF_FILE_SIGN = "FILE"
NBF_FILE_START_SKIP = 0x54 # 84
NBF_COMPRESS_START_SKIP = 0x78

# we will not use this kind of objects
class DirectoryCatalogEntry(Struct):
    _format = Format.LittleEndian
    entry_type = Type.String[4]
    unknown1 = Type.UnsignedInt
    next_entry = Type.UnsignedInt
    unknown2 = Type.String[14]
    file_start = Type.UnsignedInt
    file_size = Type.UnsignedInt
    unknown3 = Type.String[12]
    volume = Type.UnsignedByte
    unknown4 = Type.String[63]
    # filename = string

    def __init__(self, mmap, start_pos):
        self.mmap = mmap
        self.start_pos = start_pos
        self.s_size = self._struct_size

        struct_data = mmap[self.start_pos:self.start_pos + self.s_size]
        Struct.__init__(self, struct_data)

        self.filename = mmap[self.start_pos + self.s_size:].split('\0', 1)[0]
        self.s_size += len(self.filename) + 1


class FileCatalogEntry(Struct):
    _format = Format.LittleEndian
    entry_type = Type.String[4]
    unknown1 = Type.UnsignedInt
    next_entry = Type.UnsignedInt
    unknown2 = Type.String[6]
    file_size = Type.UnsignedInt
    unknown3 = Type.UnsignedInt
    file_start = Type.UnsignedInt
    unknown4 = Type.UnsignedInt
    compressed_size = Type.UnsignedInt
    unknown5 = Type.String[12]
    volume = Type.UnsignedByte
    unknown6 = Type.String[63]
    # filename = string

    def __init__(self, mmap, start_pos):
        self.mmap = mmap
        self.start_pos = start_pos
        self.s_size = self._struct_size

        struct_data = mmap[self.start_pos:self.start_pos + self.s_size]
        Struct.__init__(self, struct_data)

        self.filename = mmap[self.start_pos + self.s_size:].split('\0', 1)[0]
        self.s_size += len(self.filename) + 1


class CatalogHeader(Struct):
    _format = Format.LittleEndian
    start_signature = Type.String[4]
    zeros1 = Type.String[74]
    compression = Type.UnsignedByte
    unknown1 = Type.String[7]
    volumes = Type.UnsignedByte
    unknown2 = Type.String[71]
    # catalog_volume_name = string
    # volume_log = string
    # volume_names = list of strings

    def __init__(self, mmap, start_pos, end_pos):
        self.mmap = mmap
        self.start_pos = start_pos
        self.size = self._struct_size

        struct_data = mmap[self.start_pos:self.start_pos + self.size]
        Struct.__init__(self, struct_data)

        self.load_volume_names(mmap[self.start_pos + self.size:end_pos])

    def load_volume_names(self, rest):
        self.catalog_volume_name, self.volume_log, rest = rest.split('\0', 2)
        self.size += len(self.catalog_volume_name) + len(self.volume_log) + 2

        self.catalog_volume_name = ntpath.basename(self.catalog_volume_name)
        if self.volumes <= 1:
            self.volume_names = [self.catalog_volume_name]
            return

        self.volume_names = []
        for i in range(self.volumes):
            volume_name, rest = rest.split('\0', 1)
            self.volume_names.append(ntpath.basename(volume_name))
            self.size += len(volume_name) + 1

        self.size += 1 # I don't know why, but the header ends with 2 \0 characters instead of 1


class File(object):
    def __init__(self, filename, volume_name, start, size, compressed, compressed_size):
        self.filename = ntpath.basename(filename)
        self.volume_name = volume_name
        self.start = start
        self.size = size
        self.compressed_size = compressed_size
        self.compressed = compressed

    def save(self):
        filename = self.filename
        if os.path.exists(filename):
            count = 1
            while os.path.exists("%s.%s" % (filename, count)):
                count += 1
            filename = "%s.%s" % (filename, count)

        print "Saving %s..." % (filename)

        volume = open(self.volume_name, "rb")
        volume_filesize = os.path.getsize(self.volume_name)
        volume_mmap = mmap.mmap(
            volume.fileno(),
            volume_filesize,
            access=mmap.ACCESS_READ
        )

        if self.compressed:
            start = self.start
            end = start + self.compressed_size
            out = open(filename + ".pkz", "wb")
            out.write(volume_mmap[start:end])
        else:
            out = open(filename, "wb")
            out.write(volume_mmap[self.start+NBF_FILE_START_SKIP:self.end])

        out.close()
        volume_mmap.close()
        volume.close()

        if self.compressed:
            self.uncompress(filename)

    def uncompress(self, inp):
        try:
            proc = Popen(
                ["cat %s.pkz | ./blast" % (inp,)],
                shell=True,
                stdin=PIPE, stdout=PIPE,
                close_fds=True,
            )

            start = NBF_FILE_START_SKIP + NBF_COMPRESS_START_SKIP
            end = start + self.size
            content = proc.stdout.read()[start:end]
        except Exception, e:
            sys.stderr.write("ERROR: trying to uncompress %s (%s)." % (inp, e))
            return

        output = open(inp, 'wb')
        output.write(content)
        output.close()

        try:
            os.remove("%s.pkz" % (inp,))
        except:
            pass


# Exceptions
class InvalidFormat(Exception): pass


class Splitter(object):
    def __init__(self, catalog, patterns):
        self.catalog = catalog
        self.patterns = patterns

        try:
            self.handle = open(catalog, "rb")
        except IOError, e:
            sys.stderr.write("ERROR: cannot open %s file.\n" % (catalog))
            sys.exit(2)

        self.size = os.path.getsize(self.catalog)
        self.mmap = mmap.mmap(self.handle.fileno(), self.size, access=mmap.ACCESS_READ)

    def split(self):
        start_pos = self.mmap.find(NBF_START_SET)
        end_pos = self.mmap.find(NBF_END_SET)
        debug("Catalog set start: ", hex(start_pos))
        debug("Catalog set end: ", hex(end_pos))

        catalog_header = CatalogHeader(self.mmap, start_pos, end_pos)
        debug("Catalog Signature: ", catalog_header.start_signature)
        debug("Compression Enabled: ", catalog_header.compression != 1)
        debug("Number of volumes: ", catalog_header.volumes)
        debug("Catalog Volume Name: ", catalog_header.catalog_volume_name)
        debug("Catalog Volume Log: ", catalog_header.volume_log)
        debug("Volumes filenames:\n\t", "\n\t".join(catalog_header.volume_names))
        debug("Catalog Header Size: ", hex(catalog_header.size))

        start_entry_pos = start_pos + catalog_header.size
        debug("First Catalog Entry Position): ", hex(start_entry_pos))

        fmtstr = "  %4s  %-11s %-11s %-11s %-3s %s"
        debug(fmtstr % ("Type", "Next Pos", "Start", "Size", "Volume", "Filename"))

        current_pos = start_entry_pos
        files = []
        while current_pos < end_pos:
            if self.mmap[current_pos:current_pos + 4] == NBF_FILE_SIGN:
                entry = FileCatalogEntry(self.mmap, current_pos)

                f = File(
                    entry.filename,
                    catalog_header.volume_names[entry.volume - 1],
                    entry.file_start,
                    entry.file_size,
                    catalog_header.compression != 1,
                    entry.compressed_size,
                )
                files.append(f)

                debug(fmtstr % (
                    entry.entry_type,
                    hex(entry.next_entry),
                    hex(entry.file_start),
                    hex(entry.file_size),
                    entry.volume,
                    entry.filename))

            else:
                entry = DirectoryCatalogEntry(self.mmap, current_pos)

            current_pos += entry.s_size


        for pattern in self.patterns:
            for f in files:
                if re.search(pattern, f.filename) is not None:
                    f.save()

    def close(self):
        self.mmap.close()
        self.handle.close()


def main(args):
    if len(args) < 3:
        sys.stderr.write("""Usage: %s catalog.nbf pattern1 [pattern2 [pattern3 [...]]]
        catalog.nbf  The normally the last file in a multi volume backup
        patterns     patterns to define files to be recovered
""" % (sys.argv[0]))
        sys.exit(1)

    catalog = args[1]

    splitter = Splitter(catalog, args[1:])
    splitter.split()
    splitter.close()

if __name__ == '__main__':
    main(sys.argv)


