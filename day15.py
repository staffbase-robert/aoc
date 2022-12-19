#!/usr/bin/env python3
import os
import re


example = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

def dist(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Range:
    def __init__(self, c, d) -> None:
        self.c = c
        self.d = d
        
    def in_range(self, p):
        return dist(self.c, p) <= self.d

with open("input-15") as f:
    IN = f.read()
    # IN = example
    coords = [[(int(raw[0]), int(raw[1])), (int(raw[2]), int(raw[3]))] for raw in re.findall(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", IN, re.MULTILINE)]

    m = {}
    rs = [Range(sens, dist(sens, beac)) for sens, beac in coords]
    
    ytest = 2000000


    xmin = None
    xmax = None
    for sens, beac in coords:
        d = dist(sens, beac)
        cand = sens[0] - d
        if xmin == None:
            xmin = cand
        else:
            if xmin > cand:
                xmin = cand

        cand = sens[0] + d
        if xmax == None:
            xmax = cand
        else:
            if xmax < cand:
                xmax = cand

    res = {}

    print(xmin, xmax)
    for x in range(xmin, xmax):
        for r in rs:
            if r.in_range((x, ytest)):
                res[(x, ytest)] = "#"

    for _, beac in coords:
        res[beac] = "B"

    print(
        sum([res[k] == "#" for k in res])
    )
