#!/usr/bin/env python3
import os
import re

class Node:
    def __init__(self, val: int) -> None:
        self.card = val
        self.child_nodes = []
    def add_nodes(self, nodes: list[any]):
        self.child_nodes = nodes
    def __repr__(self) -> str:
        return f"Card {self.card}: [{', '.join([str(c.card) for c in self.child_nodes])}]"
    def mat(self):
        ret = []
        for node in self.child_nodes:
            ret.append(node)
            ret += node.mat()
        return ret

with open("input-4") as f:
    lines = f.readlines()
#     lines = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
# """.splitlines()
    lines = [re.sub("\s+", " ", line) for line in lines]
    nodes = {}
    for line in lines:
        card, nums = line.split(":")
        card = int(card.split(" ")[1].strip(" "))
        nodes[card] = Node(card)
    for li in range(len(lines)):
        line = lines[li]
        card = li + 1
        _, nums = line.split(":")
        numbers, winning_numbers = nums.split("|")
        numbers = set([int(num) for num in numbers.strip(" ").split(" ")])
        winning_numbers = set([int(num.strip(" ")) for num in winning_numbers.strip(" ").split(" ")])
        matches = numbers.intersection(winning_numbers)
        children = [nodes[card + i] for i in range(1, len(matches)+1)]
        nodes[card].add_nodes(children)

    cards = [nodes[node] for node in nodes]
    solution = len(cards)
    for card in cards:
        solution += len(card.mat())
    print(solution)