#!/usr/bin/env python3
from collections import namedtuple
from dataclasses import dataclass
import re

@dataclass
class Segment():
    left: int
    width: int

    def in_segment(self, i: int) -> bool:
        return i >= self.left and i < self.left + self.width
    
@dataclass
class SegmentList():
    segments: list[Segment]
    max_width: int = -1

    def __len__(self) -> int:
        last = self.segments[-1]
        return max(last.left + last.width, self.max_width)
    def __str__(self):
        ret = ""
        for i in range(len(self)):
            ret += "#" if any([s.in_segment(i) for s in self.segments]) else "."
        return ret
    
    def __add__(self, other: Segment) -> 'SegmentList':
        return SegmentList(self.segments + [other], self.max_width)
        

assert str(SegmentList([Segment(0,4), Segment(6,3)])) == "####..###"
            
@dataclass
class Spring():
    springs: str
    validator: list[int]

    def collect_permutations(self) -> list[SegmentList]:
        stack = [v for v in self.validator]
        permutations: list[SegmentList] = []
        def build_perms(stack: list[int], max_width: int, accum: SegmentList = SegmentList([], len(self.springs)), left=0, depth=0):
            if len(stack) == 0:
                permutations.append(accum)
                return
            width = stack.pop(0)
            if width > max_width - left:
                return
            for pos in range(left, max_width - width + 1):
                s = Segment(left=pos, width=width)
                build_perms(stack.copy(), max_width=max_width, accum=accum+s, left=pos+width+1, depth=depth+1)
        build_perms(stack, max_width=len(self.springs))
        return permutations
    
    def match(self, p: SegmentList) -> bool:
        # lol this is bad
        p_str = str(p)
        assert len(p_str) == len(self.springs)
        for i in range(len(self.springs)):
            sc = self.springs[i]
            pc = p_str[i]
            if sc == "?":
                continue
            if sc != pc:
                return False
        return True
        
    def solve(self):
        markers: set[int] = set()
        for i in range(len(self.springs)):
            if self.springs[i] == "#":
                markers.add(i)

        permutations = self.collect_permutations()
        # for p in permutations:
            # print(p, self.match(p))
        return sum([self.match(p) for p in permutations])
    

with open("input-12") as f:
    lines = f.readlines()
    lines = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()
    
    springs: list[Spring] = []
    for line in lines:
        values, validator = line.split(" ")
        springs.append(Spring(values, [int(v) for v in validator.split(",")]))


    print("part1", sum([s.solve() for s in springs]))
    part2_springs = [Spring("?".join(spring.springs * 5), spring.validator*5) for spring in springs]
    # takes to long... 