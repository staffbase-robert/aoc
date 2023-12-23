#!/usr/bin/env python3


from collections import namedtuple

Point = namedtuple("point", ["y", "x"])

class Map():
    def __init__(self, height: int, width: int, round_rocks: set[Point], cube_rocks: set[Point]) -> None:
        self.height = height
        self.width = width
        self.round_rocks = round_rocks
        self.cube_rocks = cube_rocks

    @staticmethod
    def from_raw(raw: list[str]) -> 'Map':
        height = len(raw)
        width = len(raw[0])
        round_rocks: set[Point] = set()
        cube_rocks: set[Point] = set()
        for y in range(len(raw)):
            row = raw[y]
            for x in range(len(row)):
                c = row[x]
                p = Point(y, x)
                if c == "O":
                    round_rocks.add(p)
                elif c == "#":
                    cube_rocks.add(p)
        return Map(height, width, round_rocks, cube_rocks)

    def __str__(self) -> str:
        rep = ""
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                p = Point(y,x)
                if p in self.cube_rocks:
                    row += "#"
                elif p in self.round_rocks:
                    row += "O"
                else:
                    row += "."
            rep += row + "\n"
        return rep

    # finds collider when peeking up
    def peek_up(self, pos: Point):
        current = pos
        while current.y > 0:
            new_pos = Point(current.y-1, current.x)
            if new_pos in self.cube_rocks or new_pos in self.round_rocks:
                break
            current = new_pos
        return current
    
    def tilt_north(self):
        # order cube rocks by their height
        sorted_round_rocks = sorted(list(self.round_rocks), key=lambda p: p.y)
        for rock in sorted_round_rocks:
            new_pos = self.peek_up(rock)
            self.round_rocks.remove(rock)
            self.round_rocks.add(new_pos)
        return self
            
    def rotate_right(self):
        round_rocks: set[Point] = set()
        for rock in self.round_rocks:
            p = Point(rock.x, self.height - rock.y-1)
            round_rocks.add(p)

        cube_rocks: set[Point] = set()
        for rock in self.cube_rocks:
            p = Point(rock.x, self.height - rock.y-1)
            cube_rocks.add(p)
            
        return Map(height=self.width, width=self.height, round_rocks=round_rocks, cube_rocks=cube_rocks)
            
    def rotate_left(self):
        round_rocks: set[Point] = set()
        for rock in self.round_rocks:
            p = Point(self.width - rock.x - 1, rock.y)
            round_rocks.add(p)

        cube_rocks: set[Point] = set()
        for rock in self.cube_rocks:
            p = Point(self.width - rock.x - 1, rock.y)
            cube_rocks.add(p)

        return Map(height=self.width, width=self.height, round_rocks=round_rocks, cube_rocks=cube_rocks)
            
    def score(self) -> int:
        return sum([self.height - rock.y for rock in self.round_rocks])

with open("input-14") as f:
    inp = [line.strip("\n") for line in f.readlines()]
    m = Map.from_raw(inp)
    print("part1", m.tilt_north().score())

    assert str(m.rotate_right().rotate_right().rotate_right().rotate_right()) == str(m)
    scores_before_cycle = [100410,100331,100112,99906,99813,99754,99654,99581,99475,99325,99249,99180,99184,99169,99160,99064,99009,98925,98920,98867,98826,98758,98690,98603,98538,98455,98433,98372,98340,98302,98262,98191,98149,98080,98003,97929,97844,97717,97608,97463,97331,97175,97039,96875,96745,96602,96483,96324,96225,96081,95952,95822,95725,95602,95537,95461,95389,95311,95268,95244,95231,95211,95172,95140,95121,95062,95008,94951,94895,94844,94808,94768,94716,94671,94627,94588,94563,94526,94510,94487]    
    cycle = [94491,94502,94511,94535,94560,94591,94618,94620,94615,94585,94565,94537,94510,94493,94487,94494,94517,94536,94565,94587,94610,94626,94616,94590,94561,94529,94516,94494,94492,94490,94509,94542,94566,94592,94606,94618,94622,94591,94566,94525,94508,94500,94493,94495,94505,94534,94572,94593,94611,94614,94614,94597,94567,94530,94504,94492,94499,94496,94510,94530,94564,94599,94612,94619,94610,94589,94573,94531,94509,94488]
    def predict_score(iteration: int):
        if iteration < len(scores_before_cycle):
            return scores_before_cycle[iteration]
        return cycle[(iteration - len(scores_before_cycle)) % len(cycle)]
    import tqdm
    for i in tqdm.tqdm(range(len(cycle)*2 + len(scores_before_cycle))):
        # tilt north
        m = m.tilt_north().rotate_right()
        # tilt west
        m = m.tilt_north().rotate_right()
        # tilt south
        m = m.tilt_north().rotate_right()
        # tilt east
        m = m.tilt_north().rotate_right()
        score = m.score()
        predicted_score = predict_score(i)
        assert score == predicted_score, f"score: {score} != predicted_score: {predicted_score}"
    print("part2", predict_score(1000000000-1))
