#!/usr/bin/env python3
import os
import re

def transpose(m: list[str, str]):
    tm = []
    for x in range(len(m[0])):
        tm.append([None]*len(m))
    for y in range(len(m)):
        for x in range(len(m[0])):
            tm[x][y] = m[y][x]
    return tm
    

def distance(a: tuple[int, int], b: tuple[int,int]) -> int:
    w = a[1] - b[1]
    h = a[0] - b[0]
    return int(abs(w) + abs(h))

assert distance((6,1), (11, 5)) == 9

with open("input-11") as f:
    lines = f.readlines()
#     lines = """...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....
# """.splitlines()
    y = 0
    amount = 1000000-1
    
    galaxies = []
    for line in lines:
        if line.count("#") == 0:
            y+=amount
        for x in range(len(line)):
            c = line[x]
            if c == "#":
                galaxies.append((y,x))
        y += 1
    print(galaxies)

    m = [[c for c in line] for line in lines]
    m = transpose(m)
    for mm in m:
        print(mm)

    accum = 0
    for x in range(len(m)):
        if m[x].count("#") == 0:
            for i in range(len(galaxies)):
                g = galaxies[i]
                if g[1] < x + accum:
                    continue
                g = (g[0], g[1]+amount)
                galaxies[i] = g
            accum += amount
        
    print(len(galaxies))
                    
    pairs = []
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            g = galaxies[i]
            og = galaxies[j]
            pairs.append((i, j, g, og, distance(g, og)))

    for p in pairs:
        print(f"Between galaxy {p[0]+1} and galaxy {p[1]+1}: {p[4]} ~ {p[2]} {p[3]}")
    solution = sum([p[4] for p in pairs])            
    print(solution)