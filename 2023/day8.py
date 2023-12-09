#!/usr/bin/env python3
from typing import Optional

class Node():
    def __init__(self, root: str, left: str, right: str) -> None:
        self.root: str = root
        self.left: str = left
        self.right: str = right
        self.left_node: Optional['Node'] = None
        self.right_node: Optional['Node'] = None

    def goto(self, path: str) -> 'Node':
        return self.left_node if path == "L" else self.right_node
            
with open("input-8") as f:
    lines = f.readlines()
#     lines = """RL

# # AAA = (BBB, CCC)
# # BBB = (DDD, EEE)
# # CCC = (ZZZ, GGG)
# # DDD = (DDD, DDD)
# # EEE = (EEE, EEE)
# # GGG = (GGG, GGG)
# # ZZZ = (ZZZ, ZZZ)""".splitlines()
#     lines = """LLR

# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)""".splitlines()

    instructions = lines[0].strip("\n")
    nodes: list[Node] = []
    lookup: dict[str, Node] = {}
    for line in lines[2:]:
        root, rest = line.split(" = ")
        left, right = rest.split(", ")
        left = left.strip("(")
        right = right.strip("\n")
        right = right.strip(")")
        node = Node(root, left, right)
        nodes.append(node)
        lookup[node.root] = node
    
    for node in nodes:
        node.left_node = lookup[node.left]
        node.right_node = lookup[node.right]

    node = lookup["AAA"]
    step = 0
    found = False
    while not found:
        for inst in instructions:
            step += 1
            node = node.goto(inst)
            if node.root == "ZZZ":
                found = True
                break
    print("part1", step)
    step = 0
    starter_nodes = list(filter(lambda node: node.root.endswith("A"), nodes))
    steps_to_z = []
    for node in starter_nodes:
        step = 0
        found = False
        while not found:
            for inst in instructions:
                step += 1
                node = node.goto(inst)
                if node.root.endswith("Z"):
                    steps_to_z.append(step)
                    found = True
                    break
    from math import gcd
    def lcm(l: list):
        ret = 1
        for i in l:
            ret = ret*i//gcd(ret, i)
        return ret
    print("part2", lcm(steps_to_z), steps_to_z)