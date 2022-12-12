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

class Item():
    should_norm = True
    def __init__(self, n) -> None:
        self.un = { 
            2: None, 
            3: None, 
            5: None, 
            7: None, 
            11: None, 
            13: None, 
            17: None, 
            19: None,
            23: None
        }
        for u in self.un:
            self.un[u] = n

    def norm(self):
        if self.should_norm:
            for u in self.un:
                self.un[u] %= u

    def apply(self, op):
        for u in self.un:
            self.un[u] = op(self.un[u])
        self.norm()

    def get(self, d):
        return self.un[d] % d == 0

    def __repr__(self) -> str:
        ret = ""
        for u in self.un:
            ret += f"{u} - {self.un[u]}\n"
        return ret

if __name__ == '__main__':
    with open("input-11") as f:
        m = f.read()
        # m = example

        monkes = m.split("\n\n")
        mm = []
        for monke in [monke.splitlines() for monke in monkes]:
            si = [int(m) for m in monke[1].split("Starting items: ")[1].split(", ")]
            si = [Item(s) for s in si]
            op = re.match(r"\s\sOperation\: new = old ([\+,\-\*]) ((\d+)|old)", monke[2], re.DOTALL)
            opdebug = None
            if op[2] == "old":
                if op[1] == "+":
                    op = lambda x: x + x
                    opdebug = f"add old to old"
                elif op[1] == "*":
                    op = lambda x: x * x
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
        DEBUG = False

        import time
        for round in range(R):
            for mi in range(len(mm)):
                monke = mm[mi]
                while len(monke["items"]) > 0:
                    # inspect
                    item = monke["items"].pop(0)
                    hist[mi] += 1
                    # apply op
                    item.apply(monke["op"])
                    # test
                    goto = "true" if item.get(monke["test"]) else "false"
                    mm[monke[goto]]["items"].append(item)

            round_i = round + 1
            if DEBUG:
                if round_i in [1,2,20,1000]:
                    print(f"== After round {round + 1} ==")
                    for b in hist:
                        print(f"Monkey {b} inspected items {hist[b]} times.")

                    print("")


        tot = sorted(list(hist.values()))
        
        print("result =",tot.pop() * tot.pop())