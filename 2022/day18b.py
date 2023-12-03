#!/usr/bin/env python3

import sys

sys.setrecursionlimit(200 * 200 * 200)

example="""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

OPS = [
    lambda x: (x[0] + 1, x[1], x[2]),
    lambda x: (x[0] - 1, x[1], x[2]),
    lambda x: (x[0], x[1] + 1, x[2]),
    lambda x: (x[0], x[1] - 1, x[2]),
    lambda x: (x[0], x[1], x[2] + 1),
    lambda x: (x[0], x[1], x[2] - 1),
]

class Cubegroup():
    def __init__(self, first, type = "air") -> None:
        self.cubes = set([first])
        self.type = type

    def add(self, c):
        self.cubes.add(c)

with open("input-18") as f:
    I = f.read()
    # I = example

    C = set()
    for c in [[int(c) for c in l.strip().split(",")] for l in I.splitlines()]:
        C.add((c[0], c[1], c[2]))
        
    mins = [min(c[i] for c in C) - 2 for i in range(3)]
    maxs = [max(c[i] for c in C) + 2 for i in range(3)]
    print(mins, maxs)
    groups = []
    visited = set()
    def grow(c = (mins[0], mins[1], mins[2]), group = None):
        global groups, visited
        if c in visited:
            return
        else:
            visited.add(c)
        
        for i in range(3):
            if c[i] < mins[i]:
                if group.type == "air":
                    group.type = "steam"
                return
            if c[i] > maxs[i]:
                if group.type == "air":
                    group.type = "steam"
                return

        if group == None:
            group = Cubegroup(c, "lava" if c in C else "air")
            groups.append(group)
        else:
            if (c in C) == (group.type == "lava"):
                # c is in the same type, add to the group
                group.add(c)
            else:
                # c has different type, create new group
                group = Cubegroup(c, "lava" if c in C else "air")
                groups.append(group)

        for op in OPS:
            # lava should only go to lava
            # air should be able to go to both air and lava
            new_c = op(c)
            if group.type == "lava":
                if new_c in C:
                    grow(new_c, group)
            else:
                grow(new_c, group)

    grow()

    surf_ste = 0
    surf_air = 0
    for g in groups:
        # print(g.cubes, g.type)
        if g.type == "steam":
            for cube in g.cubes:
                for op in OPS:
                    if op(cube) in C:
                        surf_ste += 1
        if g.type == "air":
            for cube in g.cubes:
                for op in OPS:
                    if op(cube) in C:
                        surf_air += 1

    surf_tot = 0
    for c in C:
        for op in OPS:
            if op(c) not in C:
                surf_tot += 1
    print(f"surface area for steam \t\t= {surf_ste}\nsurface area for air (pockets) \t= {surf_air}")
    print(f"surface of steam and air \t= {surf_air + surf_ste}")
    print("-"* 40)
    print(f"total surface area \t\t= {surf_tot}")
    print()
    print(f"number of air pockets \t\t= {sum([1 if g.type == 'air' else 0 for g in groups])}")
    print(f"number of steam surfaces \t= {sum([1 if g.type == 'steam' else 0 for g in groups])}")

    # check for consistency
    all_cubes = set()
    for g in groups:
        for c in g.cubes:
            assert(c not in all_cubes)
            all_cubes.add(c)

    print(f"number of cubes \t\t= {len(all_cubes)}")