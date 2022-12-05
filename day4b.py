#!/usr/bin/env python3
import os
import re


example = """11-39,10-10"""
def _overlap(a,b,x,y):
    return (x <= b and y >= a)

def overlap(a,b,x,y):
    return _overlap(a,b,x,y) or _overlap(x,y,a,b)
        
with open("input-4") as f:
    m = re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", f.read(), re.MULTILINE)
    m = [[int(ee) for ee in e] for e in m]
    c = 0 
    for e in m:
        ret = overlap(e[0], e[1], e[2], e[3])
        print(ret, e)
        c += ret

    print(c)

# with open("input-4") as f:
#     lines = [l.strip() for l in f.readlines()]
