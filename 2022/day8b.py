#!/usr/bin/env python3
import os
import re
import numpy as np

example = """30373
25512
65332
33549
35390"""

def calc_view_distance(p):
    ret = 0
    for vis in p:
        if vis:
            ret += 1
        else:
            ret += 1
            break
    return ret

with open("input-8") as f:
    lines = [[int(i) for i in l.strip()] for l in f.readlines()]
    lines = np.array(lines)

    scores = []
    for j in range(1,lines.shape[0]-1):
        for i in range(1,lines.shape[1]-1):
            cur = lines[j][i]
            ver = lines.T[i]
            hor = lines[j]

            vds = []
            for k in [
                (cur > hor[0:i])[::-1],
                cur > hor[i+1:],
                (cur > ver[0:j])[::-1],
                cur > ver[j+1:]
            ]:
                vd = calc_view_distance(k)
                vds.append(vd)

            scores.append(vds[0] * vds[1] * vds[2] * vds[3])

    print(max(scores))