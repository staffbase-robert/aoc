#!/usr/bin/env python3
import os
import re

            
with open("input-4") as f:
    lines = f.readlines()
#     lines = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
# """.splitlines()
    solution = 0
    for line in lines:
        card, nums = line.split(":")
        numbers, winning_numbers = nums.split("|")
        numbers = numbers.replace("  ", " ")
        winning_numbers = winning_numbers.replace("  ", " ")
        numbers = set([int(num) for num in numbers.strip(" ").split(" ")])
        winning_numbers = set([int(num.strip(" ")) for num in winning_numbers.strip(" ").split(" ")])
        exponent = len(numbers.intersection(winning_numbers)) -1 
        if exponent >= 0:
            solution += 2**(exponent)

    print(solution)