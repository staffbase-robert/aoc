#!/usr/bin/env python3
import os
import re
import sys

sys.set_int_max_str_digits(1000000)

example = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

q = lambda x: sum([int(d) for d in str(x)])

def qa(x,k):

    x = str(x)[::-1]
    is_neg = False
    if x.endswith("-"):
        is_neg = True
        x = x[0:-1]
    parts = []
    for st in range(0, len(x), k):
        en = st + k
        if en > len(x) - 1:
            en = len(x)
        parts.append(int(x[st:en][::-1]))
    
    alt = False
    res = 0
    for part in parts:
        if alt:
            res -= part
        else:
            res += part
        alt = not alt

    return res * (-1 if is_neg else 1)


def digest(x, k):
    dig = x
    while len(str(dig)) > 10:
        dig = qa(dig, k)
    return dig


rules = {
    2: lambda x: str(x)[-1] in ["0", "2", "4", "6", "8"],
    3: lambda x: q(x) % 3 == 0,
    5: lambda x: str(x)[-1] in ["0", "5"],
    7: lambda x: qa(digest(x,3), 3) % 7 == 0,
    11: lambda x: qa(digest(x,1), 1) % 11 == 0,
    13: lambda x: qa(digest(x,3), 3) % 13 == 0,
    17: lambda x: qa(digest(x,8), 8) % 17 == 0,
    19: lambda x: qa(digest(x,9), 9) % 19 == 0,
}

if __name__ == '__main__':
    with open("input-11") as f:
        m = f.read()
        # m = example

        monkes = m.split("\n\n")
        mm = []
        for monke in [monke.splitlines() for monke in monkes]:
            si = [int(m) for m in monke[1].split("Starting items: ")[1].split(", ")]
            op = re.match(r"\s\sOperation\: new = old ([\+,\-\*]) ((\d+)|old)", monke[2], re.DOTALL)
            opdebug = None
            if op[2] == "old":
                if op[1] == "+":
                    op = lambda x: x + x
                    opdebug = f"add old to old"
                elif op[1] == "*":
                    # squaring is a noop in mod N
                    op = lambda x: x
                    opdebug = f"mult old to old"
                else:
                    raise Exception("op unsupported", op[2], op[1])
            else:
                c = int(op[2])
                if op[1] == "+":
                    op = lambda x, c=c:  x + c
                    opdebug = f"add old to {c}"
                elif op[1] == "*":
                    op = lambda x, c=c: x * c
                    opdebug = f"mult old with {c}"
                else:
                    raise Exception("op unsupported", op[2], op[1])
            test = int(monke[3].split("Test: divisible by")[1])
            iftrue = int(monke[4].split("If true: throw to monkey ")[1])
            iffalse = int(monke[5].split("If false: throw to monkey ")[1])
            mm.append({"items": si, "op": op, "test": test, "true": iftrue, "false": iffalse, "debug": opdebug})

        # import json
        # print(json.dumps(mm, indent=2, default=lambda o: '<not serializable>'))

        # simulation
        hist = { i: 0 for i in range(len(mm))}
        R = 10000
        DIV = False
        DEBUG = False

        import time
        for round in range(R):
            if round % 100 == 0:
                print(f"round {round}")
            for mi in range(len(mm)):
                monke = mm[mi]
                while len(monke["items"]) > 0:
                    # inspect
                    item = monke["items"].pop(0)
                    hist[mi] += 1
                    # apply op
                    item = monke["op"](item)
                    # monke gets bored divide by 3
                    if DIV:
                        item = item // 3
                    # test
                    rule = rules[monke["test"]]
                    goto = "true" if rule(item) else "false"
                    mm[monke[goto]]["items"].append(item)
                    # print(f"item {item} thrown to {monke[goto]}")
            for mi in range(len(mm)):
                if DEBUG:
                    print(f"Monkey {mi}: {', '.join([str(it) for it in mm[mi]['items']])}")


        tot = sorted(list(hist.values()))
        
        print("result =",tot.pop() * tot.pop())