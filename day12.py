#!/usr/bin/env python3


from dijkstra import Dijkstra, Node
        

example = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

import numpy as np

def find(m, k):
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == k:
                return (x,y)


def find_all(m, k):
    ret = []
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == k:
                ret.append((x,y))

    return ret

def get_nbs(pos, bounds):
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
        
def can_goto(m, pos, newpos):
    val = m[pos[1]][pos[0]]
    new_val = m[newpos[1]][newpos[0]]

    if val == "S":
        return new_val == "a"
    
    if new_val == "E":
        return val == "z"

    return (ord(new_val) - ord(val)) <= 1


def build_graph(m):
    nodes = []
    for y in range(len(m)):
        for x in range(len(m[0])):
            a = (x,y)
            nbs = get_nbs(a, (len(m[0]), len(m)))
            for b in nbs:
                if can_goto(m, a, b):
                    nodes.append(Node((a,b), 1))
    return nodes

from multiprocessing import Pool

with open("input-12") as f:
    m = f.readlines()
    # m = example.splitlines()
    m = [[c for c in mm] for mm in m]
    graph = build_graph(m)
    the_end = find(m, "E")
    results = []
    def solve(pos):
        x,y = pos
        global results
        if m[y][x] == "a" or m[y][x] == "S":
            pos = (x,y)
            d = Dijkstra(graph, pos)
            d.solve()
            result = d.costs[the_end]["cost"]
            if m[y][x] == "S":
                print("part 1", result)
            # print(f"result for {pos} = {result}")
            return result
        else: 
            return 1e20

    with Pool(16) as p:
        x = 0
        results = p.map(solve, [(x, y) for y in range(len(m))])
        x = 2
        results += p.map(solve, [(x, y) for y in range(len(m))])
        print("part 2", min(results))
