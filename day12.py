#!/usr/bin/env python3
import os
import re

class Map():
    def __init__(self) -> None:
        pass
        

example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

import numpy as np

def find_start(m):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == "S":
                return (x,y)

def find_means(m):
    poss = {}
    for i in range(ord("a"), ord("z")):
        c = chr(i)
        for y in range(len(m)):
            for x in range(len(m[0])):
                if m[y][x] == c:
                    if c not in poss:
                        poss[c] = []
                    poss[c].append((x,y))

    ret = {}
    for k in poss:
        mean = (0,0)
        for pos in poss[k]:
            mean = (mean[0] + pos[0], mean[1] + pos[1])

        mean = (mean[0] // len(poss[k]), mean[1] // len(poss[k]))
        ret[k] = mean

    return ret

            
class Curs():
    def __init__(self, pos, val, prev = []) -> None:
        self.pos = pos
        self.val = val
        self.prev = prev
        self.visited = set(prev)

    def can_goto(self, new_val, new_pos):
        if new_pos in self.visited:
            return False

        if self.val == "S":
            return new_val == "a"
        
        if new_val == "E" and self.val != "z":
            return False

        return (ord(new_val) - ord(self.val)) <= 1

    def get(self, m):
        return m[self.pos[1]][self.pos[0]]
    
    def goto(self, next_pos, next_val):
        return Curs(next_pos, next_val, self.prev + [self.pos])

    def get_nbs(self, bounds):
        pos = self.pos
        candidates = [
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] - 1),
        ]

        ret = []
        for candidate in candidates:
            if candidate[1] >= bounds[1]:
                continue
            if candidate[1] < 0:
                continue
            if candidate[0] >= bounds[0]:
                continue
            if candidate[0] < 0:
                continue
            ret.append(candidate)

        return ret


with open("input-12") as f:
    m = f.readlines()
    # m = example.splitlines()

    m = [[c for c in mm] for mm in m]

    pos = find_start(m)
    curs = [Curs(pos, "S")]
    means = find_means(m)

    def dist(pos, val):
        global means
        nxt = chr(ord(val)+1)
        if val == "S":
            nxt = "a"
        if val == "z":
            nxt = "E"
        mean = means[nxt]
        return abs(mean[0] - pos[0]) + abs(mean[1] - pos[1])

    while True:
        if len(curs) == 0:
            break


        curs = sorted(curs, key=lambda c: ord(c.val)*10000 + dist(c.pos, c.val), reverse=True)
        cur = curs.pop(0)
        if cur.get(m) == "E":
            print(f"found exit after {len(cur.prev)} steps\npath={' '.join([f'{m[prev[1]][prev[0]]}' for prev in cur.prev])}")
            continue
        # visited.add(cur.pos)
        nbs = cur.get_nbs((len(m[0]), len(m)))
        print(cur.pos, cur.val)
        # print(f"currently at pos {cur.pos} with value {cur.val}, got {len(nbs)} possible nbs\nhistory={cur.prev}")
        for nb in nbs:
            next_val = m[nb[1]][nb[0]]
            if cur.can_goto(next_val, nb):
                nw = cur.goto(nb, next_val)
                # print("from", cur.pos, "goto", nb, "with value", next_val)
                curs.append(nw)
