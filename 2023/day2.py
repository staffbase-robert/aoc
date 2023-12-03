#!/usr/bin/env python3
import os
import re

def is_possible(totals):
    return totals['red'] <= 12 and totals['green'] <= 13 and totals['blue'] <= 14

with open("input-2") as f:
    solution = 0
    lines = f.readlines()

#     lines = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""".split("\n")
    for line in lines:
        line = line.strip('\n')
        g, r = line.split(":")
        gid = int(g.split(" ")[1])
        cube_sets = [[p.strip(" ").split(" ") for p in s.split(',')] for s in r.split(";")]

        totals = {'blue': 0, 'red': 0, 'green':0}
        rounds = 0
        for round in cube_sets:
            for reveal in round:
                c = int(reveal[0])
                color = reveal[1]
                totals[color] += c
            # print(gid, totals, is_possible(totals))
            if is_possible(totals):
                rounds += 1
            totals = {'blue': 0, 'red': 0, 'green':0}
            
        if rounds == len(cube_sets):
            solution += gid
        # print(line,"\n", cube_sets, "\n", totals, is_possible(totals), "\n")
    print(solution)