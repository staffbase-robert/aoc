#!/usr/bin/env python3

class Hist():
    def __init__(self, items: list[int]) -> None:
        self.rows = [items]
        last_row = self.rows[0]
        all_zeros = False
        while not all_zeros:
            new_row = []
            for i in range(len(last_row)-1):
                n0 = last_row[i]
                n1 = last_row[i+1]
                new_row.append(n1-n0)
            self.rows.append(new_row)
            last_row = new_row
            all_zeros = all(map(lambda x: x == 0, new_row))
        last_row = self.rows[0]
        for row in self.rows[1:]:
            assert len(row) == len(last_row) -1, f"last_row {last_row}, row {row}"
            last_row = row
    def __str__(self) -> str:
        ret = ""
        for row in self.rows:
            ret += " ".join([str(item) for item in row]) + "\n"
        return ret
    def solve(self) -> int:
        return sum([row[-1] for row in self.rows[::-1]])
    def solve2(self) -> int:
        left_most = [row[0] for row in self.rows[::-1]]
        s = 0
        m = 1
        for item in left_most[1:]:
            m *= -1 
            s += m * item
        return s * (-1 if len(self.rows) % 2 == 0 else 1)

with open("input-9") as f:
    lines = f.readlines()
#     lines = """0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45
# """.splitlines()

    rows = [[int(c) for c in line.split(" ")] for line in lines]
    h = [Hist(h) for h in rows]
    print("part1", sum([hist.solve() for hist in h]))
    print("part2", sum([hist.solve2() for hist in h]))
