#!/usr/bin/env python3
import os
import re

nums = []
lit_nums = []

tokens = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}


def find_num(line):
    r = []
    while len(line) > 0:
        for token in tokens.keys():
            if line.startswith(token):
                r.append(str(tokens[token]))
                break
        if len(r) > 0:
            break
        line = line[1:]
    while len(line) > 0:
        for token in tokens.keys():
            if line.endswith(token):
                r.append(str(tokens[token]))
                break
        if len(r) > 1:
            break
        line = line[:-1]
    return r

with open("input-1") as f:
    numbers = []
    lines = f.readlines()
    for line in lines:
        nums = find_num(line)
        print(line.strip("\n"), "",  int(''.join(nums)))
        numbers.append(int(''.join(nums)))
    print(sum(numbers))