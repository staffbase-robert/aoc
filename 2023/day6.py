#!/usr/bin/env python3
import re
            
with open("input-6") as f:
    lines = f.readlines()
#     lines = """Time:      7  15   30
# Distance:  9  40  200""".splitlines()
    lines = [re.sub("\s+", " ", line) for line in lines]
    times = [int(t) for t in lines[0].strip(" ").split(" ")[1:]]
    distances = [int(t) for t in  lines[1].strip(" ").split(" ")[1:]]

    import math
    # quadratic solution
    def solve(t,d) -> [int,int]:
        # we want to win, so we add a tiny bit of distance
        d += 1e-8 
        under_sqrt = t**2/4 - d
        if under_sqrt < 0:
            return None
        p = math.sqrt(t**2/4 -d)
        t1 = t / 2 + p
        t2 = t / 2 - p
        left, right = sorted([t1,t2])
        left += 1e-8
        right -= 1e-8
        return (math.ceil(left), math.floor(right))

    solution = 1
    for race in range(len(times)):
        time = times[race]
        distance = distances[race]
        d = solve(time, distance)
        print(d,  (d[1] - d[0] + 1))
        solution *= (d[1] - d[0] + 1)

    print("part 1")
    print(solution)
    print("part 2")
    d = solve(40817772, 219101213651089)
    print((d[1] - d[0] + 1))
    