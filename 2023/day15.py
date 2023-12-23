#!/usr/bin/env python3

# with open("input-15") as f:
    
from dataclasses import dataclass
from typing import Literal, NamedTuple, Optional


inp = "HASH"

def find_index(it, f, default=-1):
    return next((i for i, e in enumerate(it) if f(e)), default)

def calc_val(v: str) -> int:
    current_value = 0
    for c in v:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value

@dataclass
class Op:
    op_type: Literal["-", "="]
    label: str
    focal_length: Optional[int] = None

    def box(self) -> int:
        return calc_val(self.label)
        

with open("input-15") as f:
    inp = f.read()
    # inp = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    sq = inp.split(",")
    solution = 0
    for s in sq:
        v = calc_val(s)
        solution += v
    print("part1", solution)
    # inp = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


    ops: list[Op] = []
    for item in inp.split(","):
        if "-" in item:
            ops.append(Op("-", item.split("-")[0]))
        else:
            l, r = item.split("=")
            ops.append(Op("=", l, int(r)))


    Box = NamedTuple("Box", [("label", str), ("focal_length", int)])
    boxes: list[list[Box]] = [[] for i in range(256)]
    for op in ops:
        # print(f"\nAfter {op.label}{op.op_type}{op.focal_length if op.focal_length else ''}")
        if op.op_type == "=":
            new_box = Box(op.label, op.focal_length)
            current = boxes[op.box()]
            if (i := find_index(current, lambda b: op.label == b.label)) != -1:
                current[i] = new_box
            else:
                boxes[op.box()] += [new_box]
        if op.op_type == "-":
            new_lenses = list(filter(lambda b: b.label != op.label, boxes[op.box()]))
            boxes[op.box()] = new_lenses
        # for i, box in enumerate(boxes):
        #     if len(box) == 0:
        #         continue
        #     print(f"Box {i}: {[b.label + ' ' + str(b.focal_length) for b in box]}")

    solution = 0
    for i, box in enumerate(boxes):
        for j, b in enumerate(box):
            part = (i + 1) * (j + 1) * b.focal_length
            solution += part
    print("part2", solution)
