import re
import sys

from collections import defaultdict
import socket

def xcombinations(items, n):
    if n==0:
        yield []
    else:
        for i in xrange(len(items)):
            for cc in xcombinations(items[:i] + items[i + 1:], n-1):
                yield [items[i]] + cc


def check_host(host):
    try:
        socket.getaddrinfo(host, 43)
    except socket.gaierror:
        return True
    return False


consoants = 'bcdfghjklmnpqrstvwxz' # ok, i know, i know...
vogals = 'aeiouy' # ... y is not a vogal
numbers = '0123456789'
chars = consoants + vogals + numbers
rule = re.compile("^([0-9]{0,2}[a-z]{1,}|[a-z]{1,}[0-9]{0,2})$")
min_size = 5
max_size = 5
tlds = [ ".com", ".com.br", ".org", ".net" ]

hosts  = defaultdict()
hosts.default_factory = list

for size in range(min_size, max_size + 1):
    for c in xcombinations(chars, size):
        combination = ''.join(c)
        if not rule.match(combination):
            continue

        host = combination + tlds[0]
        print >>sys.stderr, "   test:", host
        if check_host(host):
            hosts[combination].append(host)
            print "added:", host

            for tld in tlds[1:]:
                if check_host(combination + tld):
                    hosts[combination].append(combination + tld)

import pprint
pprint.pprint(hosts)
