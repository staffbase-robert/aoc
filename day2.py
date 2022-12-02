#!/usr/bin/env python3
import os
import re


results = {
    "A": {
        "X": 3,
        "Y": 6,
        "Z": 0, 
    },
     "B": {
        "X": 0,
        "Y": 3,
        "Z": 6, 
    },
    "C": {
        "X": 6,
        "Y": 0,
        "Z": 3, 
    }
}

score = {
    "X": 1,
    "Y": 2,
    "Z": 3 
}

inp = """A Y
B X
C Z"""

with open("input-2") as f:
    m = re.findall(r"([A-C])\s([X-Z])", f.read(), re.MULTILINE)
    tot = 0
    for round in m:
        op = round[0]
        me = round[1]
        tot += score[me] + results[op][me]


    print(tot)

