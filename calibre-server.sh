#!/bin/bash

ulimit -n 4096
cd /opt/homebrew/bin
exec ./calibre-server --port=8888 --enable-use-sendfile $1 > ~/calibre.log
