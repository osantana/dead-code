#!/usr/bin/env python

import random

KEYMAP = [
        '.,?1',
        'abc2',
        'def3',
        'ghi4',
        'jkl5',
        'mno6',
        'pqrs7',
        'tuv8',
        'wxyz9',
]

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117241
def wrandom(lst):
    wtotal = sum([x[1] for x in lst])
    n = random.uniform(0, wtotal)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item

def create_propability_map():
    pmap = {}

    for char in ''.join(KEYMAP):
        pmap[char] = []

        # highest priority
        for key in KEYMAP:
            if key[0] != char:
                pmap[char].append((key[0], 1))

        for key in KEYMAP:
            if key[0] != char:
                pmap[char].append((key[1], 0.5))



    return pmap

keys = create_propability_map()

import pprint
pprint.pprint(keys)
# mais alta prioridade: k[0]
# mais baixa prioridade: k[-1]
# k[x] if last == k[x-1]
