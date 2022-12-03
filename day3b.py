#!/usr/bin/env python3
import os
import re

example = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

def get_score(c):
    n = ord(c)
    if n >= 97:
        n = n - 97 + 1
    else:
        n = n - 65 + 26 + 1
    return n

with open("input-3") as f:
    rooms = [l.strip() for l in f.readlines()]
    # rooms = [l.strip() for l in example.split("\n")]
    groups = [[] for _ in range(len(rooms)//3)]
    for r in range(len(rooms)):
        groups[r // 3] += [rooms[r]]

    score = 0
    for gi in range(len(groups)):
        group = groups[gi]
        common = {}
        for ri in range(3):
            room = group[ri]
            for item in room:
                if item not in common:
                    common[item] = [0,0,0]
                common[item][ri] = 1
            
        for k in common:
            if common[k] == [1,1,1]:
                score += get_score(k)

    print(score)