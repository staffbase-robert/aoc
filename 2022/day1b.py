#!/usr/bin/env python3
import os
import re


with open("input-1") as f:
    elves = f.read().split("\n\n")
    elves = [[int(i) for i in elve.split("\n")] for elve in elves]
    cals = [sum(elve) for elve in elves]
    print(sum(sorted(cals, reverse=True)[0:3]))