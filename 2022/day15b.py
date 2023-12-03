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
Sensor at x=20, y=1: closest beacon is at x=15, y=3

"""

def dist(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class Range:
    def __init__(self, c, d) -> None:
        self.c = c
        self.d = d
        
    def in_range(self, p):
        return dist(self.c, p) <= self.d

    def get_edge(self):
        edge = []
        dirs = [(1, -1), (1, 1), (-1,1), (-1,-1)]
        x = self.c[0] - self.d -1
        y = self.c[1]
        
        while dirs:
            d = dirs.pop(0)
            for _ in range((self.d+1)):
                edge.append((x,y))
                x += d[0]
                y += d[1]

        return edge

with open("input-15") as f:
    IN = f.read()
    IN = example
    # M = 4000000
    M = 20

    coords = [[(int(raw[0]), int(raw[1])), (int(raw[2]), int(raw[3]))] for raw in re.findall(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", IN, re.MULTILINE)]
    rs = [Range(sens, dist(sens, beac)) for sens, beac in coords]

    # for y in range(0, M):
    #     for x in range(0, M):
    #         collide = False
    #         for r in rs:
    #             if r.in_range((x,y)):
    #                 collide = True
    #                 break

    #         print("." if collide else "#", end="")
    #     print("")
    import tqdm
    def solve(rs, M):
        for r in tqdm.tqdm(rs):
            for d in r.get_edge():
                if d[0] < 0 or d[1] < 0:
                    continue
                if d[0] > M or d[1] > M:
                    continue
                collide = False
                for ro in rs:
                    if ro.in_range(d):
                        collide = True
                        break
                if not collide:
                    print(f"never collide at {d}, tuning frequency = {d[0] * 4000000 + d[1]}")
                    return  
    solve(rs, M)