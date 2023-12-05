#!/usr/bin/env python3

class Stage():
    def __init__(self, vals: [int, int, int]) -> None:
        self.vals = [vals[0], vals[1], vals[2]]
    def apply(self, s: int) -> int | None:
        offset = s-self.vals[1]
        if offset < 0 or s > self.vals[1] + self.vals[2]:
            return None
        return self.vals[0] + (s-self.vals[1])
    def __repr__(self) -> str:
        return f"{self.range} -> {self.result_range}"

with open("input-5") as f:
    puzzle_input = f.read()
#     puzzle_input = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4"""

    # input 
    m = puzzle_input.split("\n\n")
    seeds = [int(s) for s in m[0].split(": ")[1].split(" ")]
    stages: list[list[Stage]] = []
    for mm in m[1:]:
        stage = []
        for r in mm.splitlines()[1:]:
            rn = [int(ri) for ri in r.split(" ")]
            assert(len(rn) == 3)
            stage.append(Stage(rn))
        stage = sorted(stage, key=lambda fn: fn.vals[1])
        stages.append(stage)


    # finds score of a single seed 
    def eval_seed(s):
        val = s
        for stage in stages:
            for fn in stage:
                next_val = fn.apply(val)
                if next_val is not None:
                    val = next_val
                    break
        return val

    # part1
    print(min([eval_seed(seed) for seed in seeds]))
    # part 2
    seed_batches = []
    for s in range(0,len(seeds)-1,2):
        seed_batches.append([seeds[s], seeds[s]+seeds[s+1]-1 ])
    
    import math
    solution = math.inf
    total_steps = 0
    def eval_batch(b: [int, int]):
        global solution,total_steps
        total_steps += 1
        left = b[0]
        right = b[1]
        if right - left == 1:
            solution = min(eval_seed(left), solution)
            solution = min(eval_seed(right), solution)
            return
        mid = left + (right - left) // 2
        score_left = eval_seed(left) 
        score_mid = eval_seed(mid)
        score_right = eval_seed(right)

        mid_to_left = mid - left
        mid_to_right = right - mid

        if abs(score_left - score_mid) == mid_to_left:
            # found linear section
            low = min(score_left, score_right)
            # print(f"found linear section ~ left: {left} | mid: {mid} score_left: {score_left}, score_mid: {score_mid}, min: {low}")
            solution = min(low, solution)
        else:
            eval_batch([left, mid])
        if abs(score_right - score_mid) == mid_to_right:
            low = min(score_left, score_right)
            # print(f"found linear section ~ mid: {mid} | right: {right} score_left: {score_left}, score_mid: {score_mid}, min: {min(score_left, score_right)}")
            solution = min(low, solution)
        else:
            eval_batch([mid, right])
    for batch in seed_batches:
        eval_batch(batch)
    print(f"solution={solution} | steps={total_steps}")
