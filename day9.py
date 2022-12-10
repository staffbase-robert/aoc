#!/usr/bin/env python3
import os
import re
import numpy as np

example = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
N = 50000

def move(pos, inst):
    x, y = pos
    if inst == "R":
        x += 1
    elif inst == "L":
        x -= 1
    elif inst == "U":
        y -= 1
    elif inst == "D":
        y += 1
    
    return (x,y)

def move_tail(H, T):
    x,y = H
    x_t,y_t = T
    # same row or col
    if x == x_t or y == y_t:
        if np.abs(x_t - x) > 1:
            if x > x_t:
                x_t += 1
            else:
                x_t -=1
        if np.abs(y_t - y) > 1:
            if y > y_t:
                y_t += 1
            else:
                y_t -=1

        return (x_t, y_t)
    
    # adjacent, because diagonal
    if (np.abs(x_t - x) + np.abs(y_t - y)) <= 2:
        return T

    if x_t > x and y_t > y:
        x_t -= 1
        y_t -= 1
    elif x_t > x and y_t < y:
        x_t -= 1
        y_t += 1
    elif x_t < x and y_t > y:
        x_t += 1
        y_t -= 1
    elif x_t < x and y_t < y:
        x_t += 1
        y_t += 1

    return (x_t, y_t)

if __name__ == '__main__':
    with open("input-9") as f:
        inp = f.read()
        # inp = example
        route = re.findall(r"(\w)\s(\d+)", inp, re.MULTILINE)
        route = [(r[0], int(r[1])) for r in route]
        M = set()
        H = (0,0)
        T = [H for _ in range(9)]
        for inst in route:
            for steps in range(inst[1]):
                H = move(H, inst[0])
                for i in range(len(T)):
                    prev = H
                    if i > 0:
                        prev = T[i-1]
                    T[i] = move_tail( prev, T[i])
                M.add(T[8])

        M.add(T[8])

        print(len(M))