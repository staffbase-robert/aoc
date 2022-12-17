#!/usr/bin/env python3
import os
import re


example = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

class Valve():
    def __init__(self, name, flowrate, doors, open = False, released=0) -> None:
        self.name = name
        self.flowrate = flowrate
        self.doors = doors
        self.open = open
        self.released = released

    def update(self):
        if self.open:
            self.released += self.flowrate

    def __repr__(self) -> str:
        return f"{self.name}: released: {self.released}, flowrate: {self.flowrate}, doors: {self.doors}, {'open' if self.open else 'closed'}"

    def copy(self):
        return Valve(self.name, self.flowrate, self.doors, self.open, self.released)

class State():
    def __init__(self, valves, current, minute = 0, history=[]) -> None:
        self.minute = minute
        self.current = current
        self.valves = valves
        self.history = history

    def update(self):
        self.minute += 1
        for valve in self.valves:
            valve.update
    
    def get_result(self):
        return sum([valve.released for valve in self.valves])

    def get_paths(self):
        return [find_by_name(self.valves, door) for door in self.current.doors]

    def copy(self, nxt=None):
        new_valves = [valve.copy() for valve in self.valves]
        if nxt is not None:
            assert(type(nxt) == Valve)

        new_current = self.current if nxt is None else nxt
        return State(new_valves, new_current, self.minute, self.history + [self.current])

def deepcopy(valves):
    return [valve.copy() for valve in valves]

def find_by_name(valves, name):
    for valve in valves:
        if valve.name == name:
            return valve
    return None

def update(valves):
    for valve in valves:
        valve.update()

with open("input-16") as f:
    IN = f.read()
    IN = example
    m = [Valve(match[0], int(match[1]), match[2].split(',')) for match in re.findall(r"Valve (\w\w) has flow rate=(\d+); tunnels lead to valves (.*)", IN, re.MULTILINE)]

    state = State(m, find_by_name(m, "AA"))
    stack_count = 0
    def traverse(state):
        global stack_count
        stack_count += 1
        if state.minute == 30:
            if state.get_result() > 0:
                print(f"done, result = {state.get_result()}")
            print(stack_count)
            return

        state.update()
        if not state.current.open:
            state.current.open = True
            traverse(state.copy())
        for path in state.get_paths():
            if path == None:
                continue
            traverse(state.copy(path))

    traverse(state)