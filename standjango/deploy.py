#!/usr/bin/env python

import sys
import os
import imp
import shutil

def usage():
    print "Use: deploy.py project_dir target_dir"

def main(args):
    try:
        source = os.path.abspath(args[1])
        target = os.path.abspath(args[2])
        project_name = os.path.basename(source)
    except IndexError, ex:
        usage()
        return 1

    try:
        django = imp.find_module("django")[1]
    except ImportError, ex:
        print >>sys.stderr, "Django not found in sys.path."
        return 1

    print "Project:", source
    print "Django:", django
    print "Target:", target

    try:
        os.mkdir(target)
    except OSError, ex:
        print >>sys.stderr, "Error creating directory %s" % (target,)
        return 1

    try:
        shutil.copytree(source, os.path.join(target, project_name))
        shutil.copytree(django, os.path.join(target, "django"))
        shutil.copy("runner.py", os.path.join(target, "%s.sh" % (project_name,)))
        shutil.copy("runner.py",  os.path.join(target, "runner.pyw"))
        shutil.copy("runner.bat", os.path.join(target, "%s.bat" % (project_name,)))
    except shutil.Error, ex:
        print >>sys.stderr, "Error copying files to target dir (%s)." % (ex,)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
