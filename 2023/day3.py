#!/usr/bin/env python3
import os
import re

nbs = [
    lambda c: (c[0]+1, c[1]-1),
    lambda c: (c[0]+1, c[1]),
    lambda c: (c[0]+1, c[1]+1),
    lambda c: (c[0], c[1]+1),
    lambda c: (c[0]-1, c[1]+1),
    lambda c: (c[0]-1, c[1]),
    lambda c: (c[0]-1, c[1]-1),
    lambda c: (c[0], c[1]-1),
]

class Map():
    def __init__(self, raw) -> None:
        self.m = raw
    def __getitem__(self, c: tuple) -> str:
        assert(len(c) == 2)
        if c[0] < 0:
            return ""
        if c[0] > len(self.m)-1:
            return ""
        if c[1] < 0:
            return ""
        if c[1] > len(self.m[0])-1:
            return ""
        return self.m[c[0]][c[1]]

class Num():
    def __init__(self, y, x) -> None:
        self.x = x
        self.y = y
        self.items = []
    def add(self, c) -> None:
        self.items.append(c)
    def __repr__(self) -> str:
        return f"x: {self.x} | y: {self.y} | nums: {''.join(self.items)}"
    def val(self) -> int:
        return int("".join(self.items))
    def close_to_symbol(self, m: Map) -> bool:
        for offset in range(len(self.items)):
            x = self.x + offset
            y = self.y
            for nb in nbs:
                new_coords = nb((y,x))
                if m[new_coords] in {'-', '&', '%', '=', '$', '@', '#', '/', '*', '+'}:
                    return True
        return False
    def star_nbs(self, m: Map) -> list[tuple]:
        ret = []
        for offset in range(len(self.items)):
            x = self.x + offset
            y = self.y
            for nb in nbs:
                new_coords = nb((y,x))
                if m[new_coords] == '*':
                    ret.append(new_coords)
        return ret
            
with open("input-3") as f:
    numbers = []
    lines = f.readlines()
#     lines = """467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..""".split("\n")
    raw_map = []
    nums: list[Num] = []
    toks = set()
    for y in range(len(lines)):
        line = lines[y]
        raw_map.append([])
        num = None
        for x in range(len(line)):
            c = line[x]
            raw_map[y].append(c)
            toks.add(c)
            if c.isdigit():
                if num == None:
                    num = Num(y, x)
                num.add(c)
            else:
                if num is not None:
                    nums.append(num)
                num = None

    m = Map(raw_map)
    solution = 0
    for num in nums:
        if num.close_to_symbol(m):
            solution += num.val()
    print("part1:", solution)

    # part 2
    gears: dict[tuple, list[Num]] = {}
    for num in nums:
        stars = num.star_nbs(m)
        for star in stars:
            if star not in gears:
                gears[star] = []
            if num not in gears[star]:
                gears[star].append(num)
    solution2 = 0
    for gear in gears:
        # print(gear, gears[gear])
        if len(gears[gear]) == 2:
            solution2 += gears[gear][0].val() * gears[gear][1].val()
    print("part2:", solution2)
