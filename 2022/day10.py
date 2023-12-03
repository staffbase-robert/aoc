#!/usr/bin/env python3
import os
import re

inpu = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()

class AddOp():
    n = None
    def __init__(self, n) -> None:
        self.n = n
        
    def __repr__(self):
        return f"AddOp({self.n})"

    def do(self, value):
        return value + self.n

        
class NoOp():
    def __init__(self) -> None:
        pass
    
    def __repr__(self):
        return f"Noop"

    def do(self, value):
        return value

with open("input-10") as f:
    lines = [l.strip() for l in f.readlines()]
    # lines = inpu
    ops = []
    for line in lines:
        if line.startswith("addx"):
            ops.append(AddOp(int(line.split(" ")[1])))
        elif line == "noop":
            ops.append(NoOp())


    coi = {
        20: None, 
        60: None, 
        100: None, 
        140: None, 
        180: None, 
        220: None
    }
    X = 1
    queue = []
    cycle = 0
    while len(queue) > 0 or cycle < len(ops):
        print("start of cycle", cycle + 1)
        print("X=", X)
        if (cycle + 1) in coi:
            coi[cycle+1] = X
        # add item to queue
        if cycle < len(ops): 
            item = ops[cycle]
            if isinstance(item, AddOp):
                queue = [item, NoOp()] + queue
            else:
                queue = [ops[cycle]] + queue

        # end of cycle
        # push items from queues
        if len(queue) > 0:
            op = queue.pop()
            X = op.do(X)
            print("do ", op)
        print("end of cycle", cycle + 1)
        print("X=", X)
        cycle += 1
    print(coi)
    print(sum([item[0] * item[1] for item in coi.items()]))