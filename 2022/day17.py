#!/usr/bin/env python3
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

class TX():
    def __init__(self, ops) -> None:
        self.ops = ops
    
    def commit(self, map):
        for op in self.ops:
            op(map)

class Map():
    def __init__(self, data = {}) -> None:
        self.data = data
        self.max = 0

    def __getitem__(self, key):
        y = key[0]
        x = key[1]
        if x < 0 or x >= 7 or y < 0:
            return 2
        if y not in self.data:
            return 0
        if x not in self.data[y]:
            return 0
        return self.data[y][x]

    def set(self, key, value):
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
            if y + 1 > self.max:
                self.max = y + 1
        self.data[y][x] = value

    def __repr__(self) -> str:
        ret = ""
        if self.data == {}:
            return ret
        for y in range(self.max, -1, -1):
            for x in range(0, 7):
                ret += "#" if self[y, x] == 1 else "."
            ret += "\n"
        return ret

    # returns None, when there is a collision
    def get_tx(self, h, l, shape):
        ops = []
        for y in range(len(shape)):
            for x in range(len(shape[0])):
                if shape[y][x] == 1:
                    Y = 4 - y - 1
                    target = (l + x, h + Y)
                    if self[target[1], target[0]] >= 1:
                        return None
                    op = lambda s, target=target: s.set((target[1], target[0]), 1)
                    ops.append(op)
        return TX(ops)

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
        h = self.map.max + 4
        l = 2
        
        shape = self.shapes[self.current_shape]
        shape_count = self.shape_counts[self.current_shape]
        while True:
            # try move down, if collides -> break
            h -= 1
            tx = self.map.get_tx(h, l, shape)
            # print(f"move down h={h} l={l} diff={diff}")
            if tx == None:
                h += 1
                # apply final position
                new_tx = self.map.get_tx(h, l, shape)
                assert(new_tx != None)
                new_tx.commit(self.map)
                break

            # try move with jet, if collides -> do move back
            j = self.jets[self.current_jet]
            l += j
            tx = self.map.get_tx(h, l, shape)
            # print(f"move in jet h={h} l={l} diff={diff}")
            if tx == None:
                l -= j
            self.current_jet += 1
            self.current_jet %= len(self.jets)

        # print(f"h={h},l={l},cs={self.current_shape}")
        self.current_shape += 1
        self.current_shape %= len(self.shapes)

with open("input-17") as f:
    # jets = example
    jets = f.read()
    jets = [+1 if c == ">" else -1 for c in jets]
    t = Tetris(shapes, jets)

    from tqdm import tqdm
    heights = [0]
    for step in (pbar := tqdm(range(2022*10))):
        t.step()
        heights.append(t.map.max )
        
    print(t.map.max)


    print("trying to find frequency")
    f = None
    d = 1
    while True:
        iv = d
        cdiff = []
        for i in range(iv*2, len(heights), iv):
            y = heights[i] - heights[i-iv]
            cdiff.append(y)
            if len(cdiff) > 50:
                break
        if len(cdiff) == 1:
            break
        if len(set(cdiff)) == 1:
            print(f"found frequency for {d} ({d / len(jets)} in units of len(jets))")
            f = d
            break
        d += 1


    s = 1000000000000
    rep = (s // f) - 1
    rem = s % f
    N = heights[f]
    M = heights[f*2] - heights[f]
    R = heights[f + rem] - N
    pred = rep * M + N + R

    # remainder
    print(pred)