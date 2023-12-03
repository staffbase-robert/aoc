#!/usr/bin/env python3
import os
import re

with open("input-6") as f:
    line = [l.strip() for l in f.readlines()][0]
    marker_len = 14
    for i in range(len(line)-marker_len):
        ch = set()
        for j in range(i,i+marker_len):
            ch.add(line[j])
        if len(ch) == marker_len:
            print(f"found solution at {i+marker_len}")
            exit()
    print(line)
