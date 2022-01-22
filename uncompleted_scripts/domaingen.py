from collections import defaultdict
import socket

consoants = 'bcdfghjklmnpqrstvwxz' # ok, i know, i know...
vogals = 'aeiouy' # ... y is not a vogal
symbols = '-'
numbers = '0123456789'
chars = consoants + vogals + symbols + numbers

min_size = 1
max_size = 3

def xcombinations(items, n):
    if n==0:
        yield []
    else:
        for i in xrange(len(items)):
            for cc in xcombinations(items[:i] + items[i + 1:], n-1):
                yield [items[i]] + cc

tlds = [ ".com", ".com.br", ".org", ".net" ]
hosts  = defaultdict()
hosts.default_factory = list

for size in range(min_size, max_size + 1):
    for c in xcombinations(chars, size):
        combination = ''.join(c)
        if any( [ combination.count(v) for v in vogals ] ) and \
           any( [ combination.count(v) for v in consoants ] ) and \
           not combination.endswith(symbols) and \
           not combination.startswith(symbols):
            for tld in tlds:
                host = combination + tld
                try:
                    socket.getaddrinfo(host, 43)
                except socket.gaierror:
                    hosts[combination].append(host)
            if combination + tlds[0] in hosts[combination] and \
               combination + tlds[1] in hosts[combination]:
                print "OK", hosts[combination]
            else:
                print "  ", hosts[combination]
