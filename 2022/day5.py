#!/usr/bin/env python3
import os
import re

example = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

with open("input-5") as f:
    crates = {}
    lay = 0
    crates_in, move_instr = f.read().split("\n\n")
    for l in crates_in.split("\n")[0:-1]:
        while True:
            if len(l) == 0:
                break
            l = list(l)
            item = "".join(l[0:3])
            l = l[4:]
            m = re.match(r"(\[\w\])", item)
            if lay not in crates:
                crates[lay] = []
            crates[lay] += [None if m == None else m[1][1]]
    
        lay += 1
    
    stacks = [[] for _ in range(len(crates[0]))]
    for si in range(len(stacks)):
        for ci in range(len(crates)):
            stacks[si].append(crates[ci][si])
    for si in range(len(stacks)):
        stacks[si] = list(filter(lambda x: x != None, stacks[si]))
        stacks[si].reverse()
    m = re.findall(r"move (\d+) from (\d+) to (\d+)", move_instr)
    m = [[int(n) for n in mm] for mm in m]
    for quant, from_s, to_s in m:
        for i in range(quant):
            item = stacks[from_s-1].pop()
            stacks[to_s-1].append(item)
    result = "".join([stack[-1] for stack in stacks])
    print(result)
