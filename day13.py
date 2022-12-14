#!/usr/bin/env python3
import os
import re


example = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

def compare(lhs, rhs):
    # print(f"Compare {lhs} vs {rhs}")
    if isinstance(lhs, int) and isinstance(rhs, int):
        return lhs - rhs
    
    if isinstance(lhs, list) and isinstance(rhs, list):
        for i in range(len(lhs)):
            if i >= len(rhs):
                return 1
            
            c = compare(lhs[i], rhs[i])
            if c == 0:
                continue
        
            return c
        
        if len(lhs) == len(rhs):
            return 0
        else:
            return -1
    
    if isinstance(lhs, int):
        return compare([lhs], rhs)
    if isinstance(rhs, int):
        return compare(lhs, [rhs])

    # unreachable code ???
    assert(False)

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
with open("input-13") as f:
    I = f.read()
    # I = example
    packets = [[eval(l) for l in p.split("\n")] for p in I.split("\n\n")]


    # res = []
    # for pi in range(len(packets)):
    #     packet = packets[pi]
    #     print()
    #     if compare(packet[0], packet[1]) <= 0:
    #         res.append(pi + 1)
    #         print("in right order")
    #     else:
    #         print("not in right order")

    # print(sum(res))


    from functools import reduce
    packets = reduce(lambda x,y: x + y, packets) 
    packets += [[[2]]]
    packets += [[[6]]]

    # part 2
    res = sorted(packets, key=cmp_to_key(compare))
    for i in range(len(res)):
        print(res[i], i+1)

    print(
        res.index([[2]]) + 1,
        res.index([[6]]) + 1,
        (res.index([[2]]) + 1) * (res.index([[6]]) + 1)
    )
