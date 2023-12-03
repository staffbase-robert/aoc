#!/usr/bin/env python3
import os
import re

nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

with open("input-1") as f:
    numbers = []
    lines = f.readlines()
    lines = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""".split("\n")
    for line in lines:
        first = None
        for c in line:
            if c in nums:
                first = c
                break
        last = None
        for ci in range(len(line)-1, -1, -1):
            c = line[ci]
            if c in nums:
                last = c
                break
        assert(first is not None)
        assert(last is not None)

        numbers.append(int(first + last))
    print(sum(numbers))