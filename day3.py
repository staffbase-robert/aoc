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
    rooms = [[room[0:len(room) // 2], room[len(room) // 2:]] for room in rooms]
    score = 0
    for room in rooms:
        room1, room2 = room
        common = {}
        for item in room1:
            if item in common:
                common[item][0] = 1
            else:
                common[item] = [1,0]
        for item in room2:
            if item in common:
                common[item][1] = 1
            else:
                common[item] = [0,1]

        for k in common:
            if common[k] == [1,1]:
                score += get_score(k)

    print(score)