#!/usr/bin/env python3
import os
import re


example = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
6-8,9-44
2-6,4-8"""

def _contains(a,b,x,y):
    print(a,b,x,y,x >= a and y <= b)
    return x >= a and y <= b
        
def contains(a,b,x,y):
    return _contains(a,b,x,y) or _contains(x,y,a,b)

with open("input-4") as f:
    m = re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", f.read(), re.MULTILINE)
    m = [[int(ee) for ee in e] for e in m]
    c = 0 
    for e in m:
        ret = contains(e[0], e[1], e[2], e[3])
        print(ret, e)
        c += contains(e[0], e[1], e[2], e[3])

    print(c)

# with open("input-4") as f:
#     lines = [l.strip() for l in f.readlines()]
