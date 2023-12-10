#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Optional

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

NORTH = "N"
SOUTH = "S"
WEST = "W"
EAST = "E"

NORTHEAST = "NE"
NORTHWEST = "NW"
SOUTHEAST = "SE"
SOUTHWEST = "SW"

OPP = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

MOV_TO_ACT = {
    NORTH: lambda p: (p[0]-1 , p[1]),
    SOUTH: lambda p: (p[0]+1 , p[1]),
    EAST: lambda p: (p[0] , p[1]+1),
    WEST: lambda p: (p[0] , p[1]-1),
    NORTHEAST: lambda p: (p[0]-1 , p[1]+1),
    NORTHWEST: lambda p: (p[0]-1 , p[1]-1),
    SOUTHEAST: lambda p: (p[0]+1 , p[1]+1),
    SOUTHWEST: lambda p: (p[0]+1 , p[1]-1),
}

RULES = {
    "|": {
        NORTH: SOUTH,
        SOUTH: NORTH,
    },
    "-": {
        WEST: EAST,
        EAST: WEST,
    },
    "L": {
        NORTH: EAST,
        EAST: NORTH,
    },
    "J": {
        NORTH: WEST,
        WEST: NORTH,
    },
    "7": {
        SOUTH: WEST,
        WEST: SOUTH,
    },
    "F": {
        SOUTH: EAST,
        EAST: SOUTH,
    }
}


INSIDE = "ins"
OUTSIDE = "out"
TOK_TO_INSIDE_OUTSIDE: dict[str, dict[str, dict[str, list[str]]]] = {
    "|": {
        SOUTH: { INSIDE: [WEST], OUTSIDE: [EAST] },
        NORTH: { INSIDE: [EAST], OUTSIDE: [WEST] }
    },
    "-": {
        WEST: { INSIDE: [NORTH], OUTSIDE: [SOUTH] },
        EAST: { INSIDE: [SOUTH], OUTSIDE: [NORTH] },
    },
    "L": {
        EAST: { INSIDE: [EAST, SOUTH], OUTSIDE: [] },
        NORTH: { INSIDE: [], OUTSIDE: [EAST, SOUTH] }
    },
    "J": {
        WEST: { OUTSIDE: [SOUTH, EAST], INSIDE: [] },
        NORTH: { INSIDE: [SOUTH, EAST], OUTSIDE: [] }
    },
    "7": {
        WEST: { INSIDE: [NORTH, EAST], OUTSIDE: []},
        SOUTH: { INSIDE: [], OUTSIDE: [NORTH, EAST]}
    },
    "F": {
        SOUTH: {INSIDE: [WEST, NORTH], OUTSIDE: []},
        EAST: {INSIDE: [], OUTSIDE: [WEST, NORTH]}
    }
}


MOVS = [NORTH, SOUTH, WEST, EAST]
EXTRA_MOVS = [NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST]

class Map():
    def __init__(self, rows: list[list[str]]) -> None:
        self.rows = rows
    def __getitem__(self, p: tuple[int, int]) -> Optional[str]:
        y, x = p[0], p[1]
        if self.is_outside(y,x):
            return None
        item = self.rows[y][x]
        return item
    def is_outside(self, y, x) -> bool:
        if y >= self.ymax():
            return True
        if x >= self.xmax():
            return True
        if y < 0:
            return True
        if x < 0:
            return True
        return False
    def ymax(self) -> int:
        return len(self.rows)
    def xmax(self) -> int:
        return len(self.rows[0])
    def Y(self) -> range:
        return range(self.ymax())
    def X(self) -> range:
        return range(self.xmax())


with open("input-10") as f:
    lines = f.readlines()
#     lines = """.F----7F7F7F7F-7....
# .|F--7||||||||FJ....
# .||.FJ||||||||L7....
# FJL7L7LJLJ||LJ.L-7..
# L--J.L7...LJS7F-7L7.
# ....F-J..F7FJ|L7L7L7
# ....L7.F7||L7|.L7L7|
# .....|FJLJ|FJ|F7|.LJ
# ....FJL-7.||.||||...
# ....L---J.LJ.LJLJ...""".splitlines()
    
#     lines = """...........
# .S-------7.
# .|F-----7|.
# .||.....||.
# .||.....||.
# .|L-7.F-J|.
# .|..|.|..|.
# .L--J.L--J.
# ...........
# """.splitlines()
    
    
    
    m = [[c for c in line] for line in lines]
    start = None
    for y in range(len(m)):
        row = m[y]
        for x in range(len(row)):
            item = row[x]
            if item == "S":
                start = (y,x)

    M = Map(m)
    initial_nbs = [(MOV_TO_ACT[mov](start), OPP[mov]) for mov in MOVS]
    loops = []
    for nb in initial_nbs:
        loop = []
        pos = nb[0]
        come_from = nb[1]
        while True:
            tok = M[pos]
            if tok == None or tok == ".":
                break
            if tok == "S":
                loops.append(loop)
                break
            rule = RULES[tok]
            if come_from not in rule:
                break
            go_to = rule[come_from]
            loop.append((pos, come_from))
            pos = MOV_TO_ACT[go_to](pos)
            come_from = OPP[go_to]
    assert len(loops) == 2
    print("part1", len(loops[0]) // 2 + 1)

    loop = loops[0]
    prev_point = None
    points = {
        INSIDE: set(),
        OUTSIDE: set(),
    }
    for l in loop:
        p = l[0]
        come_from = l[1]
        tok = M[p]
        for what in [INSIDE, OUTSIDE]:
            movs = TOK_TO_INSIDE_OUTSIDE[tok][come_from][what]
            for point in [MOV_TO_ACT[mov](p) for mov in movs]:
                if point in [l[0] for l in loop]:
                    continue
                if M.is_outside(point[0], point[1]):
                    continue
                points[what].add(point)

    assert len(points[INSIDE].intersection(points[OUTSIDE])) == 0
    assert len(points[INSIDE].intersection(set(loop))) == 0
    assert len(points[OUTSIDE].intersection(set(loop))) == 0
    picture = ""
    for y in M.Y():
        row = ""
        for x in M.X():
            p = (y,x)
            if p in [l[0] for l in loop]:
                row += "x"
            elif p in points[INSIDE]:
                row += "I"
            elif p in points[OUTSIDE]:
                row += "O"
            else:
                row += "."
        picture += row
        picture += "\n"

    print(f"inside points on boundary = {len(points[INSIDE])}")
    print("inside points can be counted manually:")
    print(picture)
