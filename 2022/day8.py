#!/usr/bin/env python3
import os
import re
import numpy as np

example = """30373
25512
65332
33549
35390"""

with open("input-8") as f:
    lines = [[int(i) for i in l.strip()] for l in f.readlines()]
    lines = np.array(lines)

    result = (lines.shape[0] + lines.shape[1]) * 2 - 4
    for j in range(1,lines.shape[0]-1):
        for i in range(1,lines.shape[1]-1):
            cur = lines[j][i]
            ver = lines.T[i]
            hor = lines[j]
            is_visible = np.all(cur > hor[0:i]) or np.all(cur > hor[i+1:]) or np.all(cur > ver[0:j]) or np.all(cur > ver[j+1:])
            result += 1 if is_visible else 0

    print(result)

