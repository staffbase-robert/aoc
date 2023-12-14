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
    lines = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines()
    vertical_expansion = []
    line_length = len(lines[0])
    for line in lines:
        if line.count("#") == 0:
            vertical_expansion.append("."*line_length)
        vertical_expansion.append(line)


    transposed_m = transpose(vertical_expansion)
    line_length = len(transposed_m[0])
    horizontal_expansion = []
    for line in transposed_m:
        if line.count("#") == 0:
            horizontal_expansion.append("."*line_length)
        horizontal_expansion.append(line)

    m = transpose(horizontal_expansion)

    galaxies = []
    for y in range(len(m)):
        for x in range(len(m[0])):
            p = (y,x)
            if m[y][x] == "#":
                galaxies.append(p)

    print(galaxies)
    exit()
    pairs = []
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            g = galaxies[i]
            og = galaxies[j]
            pairs.append((i, j, g, og, distance(g, og)))

    for p in pairs:
        print(f"Between galaxy {p[0]+1} and galaxy {p[1]+1}: {p[4]}")
    solution = sum([p[4] for p in pairs])            
    print(solution)