#!/usr/bin/env python3

# with open("input-15") as f:
    
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Callable, Literal, NamedTuple, Optional

Point = NamedTuple("P", [("y", int), ("x", int)])

@dataclass
class Tile:
    pos: Point
    tile_type: Literal[".", "\\", "/", "-", "|"]
    energized: bool = False
    touched: Optional[Literal["N", "S", "E", "W"]] = None

@dataclass
class Map:
    width: int
    height: int
    points: dict[Point, Tile] = field(default_factory=dict)

    @staticmethod
    def from_raw(r: list[str]) -> 'Map':
        m = Map(len(r), len(r[0]))
        for y, line in enumerate(r):
            for x, c in enumerate(line):
                assert c in [".", "\\", "/", "-", "|"], c
                pos = Point(y,x)
                t = Tile(pos, c)
                m.points[pos] = t
        assert len(m.points) == m.width * m.height
        return m
    
    def __str__(self) -> str:
        s = ""
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                pos = Point(y,x)
                tile = self.points[pos]
                if tile.touched is not None:
                    line += "#"
                else:
                    line += "."
            s += "\n" + line
        return s

    def score(self) -> int:
        return sum([p.energized for p in self.points.values()])

MOV = {
    "N": lambda p: (p[0]-1 , p[1]),
    "S": lambda p: (p[0]+1 , p[1]),
    "E": lambda p: (p[0] , p[1]+1),
    "W": lambda p: (p[0] , p[1]-1),
}

class Head:
    def __init__(self, pos: Point, dir: Literal["N", "S", "E", "W"]) -> None:
        self.pos = pos
        self.dir = dir

    ID = lambda h: [h.nav(h.dir)]
    TILE_ACT: dict[str, dict[str, Callable[['Head'], list['Head']]]] = {
        ".": {"N": ID, "S": ID, "W": ID, "E": ID},
        "|": {"N": ID, "S": ID, "W": lambda h: [h.nav("N"), h.nav("S")], "E": lambda h: [h.nav("N"), h.nav("S")]},
        "-": {"N": lambda h: [h.nav("E"), h.nav("W")], "S": lambda h: [h.nav("E"), h.nav("W")], "E": ID, "W": ID},
        "/": {"N": lambda h: [h.nav("E")], "S": lambda h: [h.nav("W")], "W": lambda h: [h.nav("S")], "E": lambda h: [h.nav("N")]},
        "\\": {"N": lambda h: [h.nav("W")], "S": lambda h: [h.nav("E")], "W": lambda h: [h.nav("N")], "E": lambda h: [h.nav("S")]}
    }

    def mov(self, m: Map) -> list['Head']:
        self.pos = MOV[self.dir](self.pos)
        if self.pos not in m.points:
            return []
        tile = m.points[self.pos]
        tile.energized = True
        tile.touched = self.dir
        fn = self.TILE_ACT[tile.tile_type][self.dir]

        return fn(self)
    def nav(self, direction: Literal["N", "S", "E", "W"]) -> 'Head':
        return Head(self.pos, direction)
    def __repr__(self) -> str:
        return f"{self.pos}: {self.dir}"


with open("input-16") as f:
    inp = f.read().split("\n")
    def solve(p: Point, heading: Literal["N", "S", "E", "W"]):
        m = Map.from_raw(inp)
        heads = [Head(p, heading)] 
        seen: set[tuple[Point, str]] = set()
        while len(heads) > 0:
            next_heads = []
            for head in heads:
                new_heads = head.mov(m)
                for head in new_heads:
                    if (head.pos, head.dir) in seen:
                        continue
                    next_heads.append(head)
                seen.add((head.pos, head.dir))
            heads = next_heads
            next_heads = []
        return m.score()
    
    print("part1", solve((0,-1), "E"))

    ics = []
    for y in range(0, len(inp)):
        ics.append(((y, -1), "E"))
        ics.append(((y, len(inp[0])), "W"))
    for x in range(0, len(inp[0])):
        ics.append(((-1, x), "S"))
        ics.append(((len(inp), x), "N"))

    import tqdm
    best = -1
    for param in tqdm.tqdm(ics):
        score = solve(*param)
        if score > best:
            best = score

    print("part2", best)
    





