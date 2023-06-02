#!/usr/bin/env python

import os
import sys
import subprocess

filename = sys.argv[1]
outfilename = f'{filename}-out.pdf'
size = os.path.getsize(filename)

inp = open(filename, 'rb')
inp.seek(os.path.getsize(outfilename))

found = False

while not found:
    with open(outfilename, 'ab') as out:
        if not out.write(inp.read(1)):
            break

    chunk_size = os.path.getsize(outfilename)
    print(f'\rCheck {outfilename} with chunk size {chunk_size} of {size} ({(chunk_size/size)*100:3.2f}%)...', end='')

    try:
        subprocess.run(['pdfcpu', 'validate', outfilename], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        continue
    else:
        found = True

if found:
    print(f'\nFound: {outfilename}')
else:
    print(f'\nFailed {filename}')
    os.remove(outfilename)
