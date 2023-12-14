#!/usr/bin/env python3

import copy

def transpose(m: list[str]):
    tm = []
    for x in range(len(m[0])):
        row = []
        for y in range(len(m)):
            row += [m[y][x]]
        tm.append(''.join(row))
    return tm

def collect_nbs(n: int, max_bit_depth: int) -> list[int]:
    return [n ^ 1 << i for i in range(max_bit_depth)]

class Map():
    def __init__(self, m: list[str]) -> None:
        self.data = m
        self.width = None if len(m) == 0 else len(m[0])
        self.height = len(m)
        self.bm = self.to_bitmap(m)

    def to_bitmap(self, m: list[str]) -> dict[int, list[int]]:
        rows: dict[int, list[int]] = {}
        for r in range(len(m)):
            l = m[r]
            n = 0
            for i in range(len(l)):
                n += (1 << i) if l[i] == "#" else 0
            if n not in rows:
                rows[n] = []
            rows[n] += [r]
        return rows
    
    def mutations(self) -> list['Map']:
        new_bms = []
        for val, rn in self.bm.items():
            for new_val in collect_nbs(val, self.width):
                new_rows = copy.deepcopy(self.bm)
                del new_rows[val]
                if new_val not in new_rows:
                    new_rows[new_val] = []
                new_rows[new_val] += rn
                new_bms.append(new_rows)

        new_maps = []
        for bm in new_bms:
            m = Map([])
            m.data = None
            m.width = self.width
            m.height = self.height
            m.bm = bm
            new_maps.append(m)

        return new_maps

    def find_mirrors(self) -> list[int]:
        pot_mir: dict[int, int] = {}
        for row in self.bm.values():
            if len(row) == 1:
                continue
            for i in range(len(row)-1):
                for j in range(i+1, len(row)):
                    left, right = sorted([row[i], row[j]])
                    if (left+right)%2 == 0:
                        continue
                    mid = (right - left) // 2
                    mir = left + mid
                    if mir not in pot_mir:
                        pot_mir[mir] = 0
                    pot_mir[mir] += 1

        mirs = []
        for pos, amount in pot_mir.items():
            min_amount = min(pos+1, (self.height - (pos + 1)))
            if amount >= min_amount:
                mirs.append(pos)
        return mirs
    
    def solve_p1(self) -> int:
        mirrors = self.find_mirrors()
        assert len(mirrors) <= 1, mirrors
        return sum([mir+1 for mir in mirrors])
    
    def solve_p2(self) -> int:
        print()
        base = set(self.find_mirrors())
        new_mirs = set([])
        mutations = self.mutations()
        assert len(mutations) <= self.width * self.height, mutations
        for mutation in mutations:
            mutm = mutation.find_mirrors()
            for mutm in mutm:
                if mutm in base:
                    continue
                new_mirs.add(mutm)
        return sum([mir+1 for mir in new_mirs])


with open("input-13") as f:
    inp = f.read()
#     inp = """#.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#"""
#     inp = """#...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#"""

    patterns = inp.split("\n\n")
    mats = [pat.strip("\n").split("\n") for pat in patterns]
    maps = [Map(mat) for mat in mats]
    tmaps = [Map(transpose(mat)) for mat in mats]

    print("part1",sum([m.solve_p1() for m in maps] * 100 + [m.solve_p1() for m in tmaps]) )
    print("part2",sum([m.solve_p2() for m in maps] * 100 + [m.solve_p2() for m in tmaps]) )
    