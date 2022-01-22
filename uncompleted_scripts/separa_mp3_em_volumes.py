#!/usr/bin/env python

import os
import sys

if len(sys.argv) < 2:
    print "use: %s diretorio" % sys.argv[0]
    sys.exit(1)

f = os.popen("du -sk %s/*" % sys.argv[1])

#CD = 703 * 1024
CD = 4350 * 1000 # DVD

def print_cd(cd):
    size = 0

    for directory in cd:
        print "%5dMB %s" % (directory.size / 1024, directory.name)
        size += directory.size

    print "%s (%5dMB + %5dMB)\n" % ('-' * 40, size / 1024, (CD - size) / 1024)


class Directory(object):
    def __init__(self, size, name):
        self.name = os.path.basename(name)
        self.size = int(size)
        self.saved = False

    def __cmp__(self, other):
        return other.size - self.size

res = []
for line in f:
    s, n = line.split()
    res.append(Directory(s,n))

res.sort()


cd = []
total_size = 0
cd_number = 1

while True:
    lst = [ x for x in res if not x.saved ]
    if not lst:
        break

    start = True
    for i in lst:
        if i.size > CD:
            i.saved = 'impossivel'
            continue


        if total_size + i.size > CD and not start:
            continue

        if total_size + i.size > CD:
            # fechou o cd
            print "CD #%3d" % cd_number
            print "-------"
            print_cd(cd)
            cd = [i]
            total_size = i.size
            cd_number += 1
        else:
            # adiciona mais um
            cd.append(i)
            total_size += i.size

        i.saved = True
        start = False

print "CD #%3d" % cd_number
print "-------"
print_cd(cd)

print "Impossivel gravar"
print "-----------------"
total_size = 0
for directory in [ x for x in res if x.saved == 'impossivel' ]:
    print "%5dMB %s" % (directory.size / 1024, directory.name)
    total_size += directory.size
print "%5dGB TOTAL" % (total_size / 1024 / 1024)

f.close()

