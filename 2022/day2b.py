#!/usr/bin/env python3
import os
import re

op_picked = {
    "X": {
        "A": 3,
        "B": 1,
        "C": 2,
    },
    "Y": {
        "A": 1,
        "B": 2,
        "C": 3,
    },
    "Z": {
        "A": 2,
        "B": 3,
        "C": 1,
    },
    
}

score = {
    "X": 0,
    "Y": 3,
    "Z": 6
}

inp = """A Y
B X
C Z"""

with open("input-2") as f:
    m = re.findall(r"([A-C])\s([X-Z])", f.read(), re.MULTILINE)
    tot = 0
    for round in m:
        op = round[0]
        res = round[1]
        tot += score[res] + op_picked[res][op]


    print(tot)

