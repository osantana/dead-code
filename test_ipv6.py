#!/bin/env python3

import ssl
import socket

addrs = (
    ("google.com", "2a00:1450:4001:81e::200e"),
    ("pypi.org", "2a04:4e42:200::223"),
    ("gnu.org", "2001:470:142:3::a"),
)

for name, addr in addrs:
    print(name, addr)
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 6)
    s.connect((addr, 443, 0, 0))
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    s.sendall("GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(name).encode("ascii"))

    while True:
        new = s.recv(4096)
        if not new:
            s.close()
            break
        print(new)
