#!/usr/bin/env python3
from copy import deepcopy

example = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

shapes = [
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
    ],
    [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0],
    ],
       [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
    ],
]

class Map():
    def __init__(self, data = {}) -> None:
        self.data = data
        self.trimmed_height = 0

    def __getitem__(self, key):
        y = key[0]
        x = key[1]
        if y not in self.data:
            return 0
        if x not in self.data[y]:
            return 0
        return self.data[y][x]

    def __setitem__(self, key, value):
        y = key[0]
        x = key[1]
        if x < 0:
            return
        if x >= 7:
            return
        if y < 0:
            return
        if y not in self.data:
            self.data[y] = {}
        self.data[y][x] = value

    def count(self):
        tot = 0
        for y in self.data:
            for x in self.data[y]:
                tot += self.data[y][x]
        return tot

    def max(self):
        if self.data == {}:
            return 0
        return max([k for k in self.data]) + 1

    def copy(self):
        return Map(deepcopy(self.data))

    def find_bottom(self):
        start_height = self.max()
        lowpoints = []
        # find lowpoints
        for x in range(7):
            y = start_height
            while True:
                if y <= 0:
                    lowpoints.append(0)
                    break
                if self[y,x] == 1:
                    lowpoints.append(y)
                    break
                y -= 1
        lowpoint = min(lowpoints) - 100
        if lowpoint < 0:
            lowpoint = 0
        return lowpoint

    def trim_map(self):
        bot = self.find_bottom()
        for y in range(0,bot):
            if y in self.data:
                del self.data[y]
        
        self.trimmed_height += bot
        return bot

    def __repr__(self) -> str:
        ret = ""
        if self.data == {}:
            return ret
        for y in range(self.max(), -1, -1):
            for x in range(0, 7):
                ret += "#" if self[y, x] == 1 else "."
            ret += "\n"
        return ret

    def apply(self, h, l, shape, mult=1):
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x] == 1:
                    Y = 4 - y - 1
                    # print(f"debug apply h={h} y={y} Y={Y}")
                    self[h + Y, l + x] = 1

class Tetris():
    def __init__(self, shapes, jets) -> None:
        self.shapes = shapes
        self.shape_counts = [4, 5, 5, 4, 4]
        self.jets = jets
        self.current_shape = 0
        self.current_jet = 0
        self.top = 0
        self.map = Map()


    def step(self):
        h = self.map.max() + 4
        l = 2
        
        shape = self.shapes[self.current_shape]
        shape_count = self.shape_counts[self.current_shape]
        while True:
            # try move down, if collides -> break
            h -= 1
            tmp_map = self.map.copy()
            tmp_map.apply(h, l, shape)
            diff = tmp_map.count() - shape_count - self.map.count()
            # print(f"move down h={h} l={l} diff={diff}")
            if diff < 0:
                h += 1
                # apply final position
                self.map.apply(h, l, shape)
                break

            # try move with jet, if collides -> do move back
            j = self.jets[self.current_jet]
            l += j
            tmp_map = self.map.copy()
            tmp_map.apply(h, l, shape)
            diff = diff = tmp_map.count() - shape_count - self.map.count()
            # print(f"move in jet h={h} l={l} diff={diff}")
            if diff < 0:
                l -= j
            self.current_jet += 1
            self.current_jet %= len(self.jets)

        # print(f"h={h},l={l},cs={self.current_shape}")
        self.current_shape += 1
        self.current_shape %= len(self.shapes)
with open("input-17") as f:
    jets = example
    # jets = f.read()
    jets = [+1 if c == ">" else -1 for c in jets]
    t = Tetris(shapes, jets)

    from tqdm import tqdm
    heights = []
    for step in (pbar := tqdm(range(2022))):
        t.step()
        heights.append(t.map.max() + t.map.trimmed_height)
        
    print(t.map)
    print(t.map.max() + t.map.trimmed_height)
    