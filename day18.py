#!/usr/bin/env python3

example="""2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

with open("input-18") as f:
    I = f.read()
    I = example

    C = set()
    for c in [[int(c) for c in l.strip().split(",")] for l in I.splitlines()]:
        C.add((c[0], c[1], c[2]))

    S = 0
    for c in C:
        s = 0
        for op in [
            lambda x: (x[0] + 1, x[1], x[2]),
            lambda x: (x[0] - 1, x[1], x[2]),
            lambda x: (x[0], x[1] + 1, x[2]),
            lambda x: (x[0], x[1] - 1, x[2]),
            lambda x: (x[0], x[1], x[2] + 1),
            lambda x: (x[0], x[1], x[2] - 1),
        ]:
            if op(c) not in C:
                print("counting ", c)
                s += 1
        S += s
    print(S)
