#!/usr/bin/env python3
import os
import re

class Simulation():
    def __init__(self, paths) -> None:
        self.sand = None
        self.map = {}

        for path in paths:
            last = path.pop(0)
            cur = last
            while path:
                nxt = path.pop(0)
                while cur != nxt:
                    self.map[(cur[0], cur[1])] = "rock"
                    if nxt[0] == cur[0]:
                        cur[1] += 1 if cur[1] < nxt[1] else -1
                    elif nxt[1] == cur[1]:
                        cur[0] += 1 if cur[0] < nxt[0] else -1
                    else:
                        assert(False)
                self.map[(cur[0], cur[1])] = "rock"

    def gravity(self):
        nxt = (self.sand[0], self.sand[1] + 1)
        if nxt not in self.map:
            return nxt
        
        left = (nxt[0] - 1, nxt[1]) 
        if left not in self.map:
            return left

        right = (nxt[0] + 1, nxt[1]) 
        if right not in self.map:
            return right

        # can't move
        return self.sand

    def step(self):
        if self.sand == None:
            self.sand = (500,0)

        while True:
            nxt = self.gravity()
            if nxt == (500,0):
                return True
            if nxt == self.sand:
                self.map[nxt] = "sand"
                self.sand = None
                break
            self.sand = nxt
        return False
    
    def __repr__(self) -> str:
        xmin = min(self.map, key=lambda p: p[0])[0]
        ymin = 0
        xmax = max(self.map, key=lambda p: p[0])[0]
        ymax = max(self.map, key=lambda p: p[1])[1]

        ret = ""
        for yi in range(ymax-ymin + 1):
            ret += "\n"
            for xi in range(xmax-xmin + 1):
                x = xmin + xi
                y = ymin + yi
                if (x,y) in self.map:
                    ret += "#" if self.map[(x,y)] == "rock" else "+"
                else:  
                    ret += "."
        # return f"{xmin},{xmax},{ymin},{ymax}"
        s = sum(self.map[p] == "sand" for p in self.map)
        ret += f"\ntotal sand = {s}"
        return ret
                

example = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


with open("input-14") as f:
    IN = f.read()
    # IN = example

    paths = [[[int(s) for s in c.split(',')] for c in l.split(" -> ")]  for l in IN.splitlines()]
    paths.append([[100, 163],[800, 163]])
    # expand paths
    s = Simulation(paths)
    xmin = min(s.map, key=lambda p: p[0])[0]
    xmax = max(s.map, key=lambda p: p[0])[0]
    ymax = max(s.map, key=lambda p: p[1])[1]

    print(ymax, (xmin,xmax))

    print(s)
    while not s.step():
        pass
    print(s)
