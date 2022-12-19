#!/usr/bin/env python3
import os
import re
import copy

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

def find_by_name(valves, name):
    for valve in valves:
        if valve.name == name:
            return valve
    return None
class Valve():
    def __init__(self, name, flowrate, doors, reward=0) -> None:
        self.name = name
        self.flowrate = flowrate
        self.doors = doors
        self.connections = None
        self.reward = reward

    def connect(self, all_valves):
        self.connections = [(find_by_name(all_valves, door), 1) for door in self.doors]
        if self.flowrate != 0:
            new_valve = Valve(f"{self.name}-OV", 0, [self.name], self.flowrate)
            self.connections.append((new_valve, 1))
            all_valves.append(new_valve)

    def __repr__(self) -> str:
        return f"{self.name}: flowrate: {self.flowrate}, doors: {self.doors}, reward: {self.reward}"


def simplify(valve, visited=set()):
    visited.add(valve)
    for ci in range(len(valve.connections)):
        edge = valve.connections[ci]
        con, cost = edge
        if con.flowrate == 0:
            inherited = list(filter(lambda edge: edge[0].name != valve.name, child.connections))
            inherited = [(inh[0], inh[1] + cost) for inh in inherited]
            valve.chonections = valve.chonections[0:ci] + valve.chonections[ci+1:] + inherited
    for con, _ in valve.connections:
        if con not in visited:
            simplify(con, visited=visited)

import graphviz

def visualize(valve):
    e = graphviz.Graph('ER', filename='er.gv', engine='neato')
    def draw_edges(valve, visited = set()):
        visited.add(valve)
        e.node(valve.name, label=f"{valve.name} - {valve.reward}")
        for con, cost in valve.connections:
            e.edge(valve.name, con.name, label=f"{cost}", len="3")

        for con, _ in valve.connections:
            if con not in visited:
                draw_edges(con, visited=visited)

    draw_edges(valve)
    return e

with open("input-16") as f:
    # IN = f.read()
    IN = example
    valves = [Valve(match[0], int(match[1]), match[2].split(', ')) for match in re.findall(r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)", IN, re.MULTILINE)]
    for valve in valves:
        valve.connect(valves)


    # simplify(valves[0])
    # visualize(valves[0]).view()

    paths = []
    
    valves_with_reward = list(filter(lambda v: v.reward > 0, valves))
    for v in valves_with_reward:
        print(v)

    def find_routes(v, target):
        def traceback(v, target, routes, history=[]):
            history.append(v)
            for con, _ in v.connections:
                if con == target:
                    routes.append(history)
                else:
                    if con not in history:
                        traceback(con, target, routes, copy.copy(history))

        routes = []
        traceback(v, target, routes)
        return routes

    max_clock = 30

    best = -1
    def nav(current, targets, minute=0, rewards=[], paths=[]):
        global best
        for vi in range(len(targets)):
            v = targets[vi]
            routes = find_routes(current, v)
            shortest = min(routes, key=lambda r: len(r))
            remaining = targets[0:vi] + targets[vi+1:]
            clock = minute + len(shortest)
            new_paths = copy.copy(paths)
            new_paths.append(shortest)
            if len(remaining) > 0:
                if clock <= max_clock:
                    new_rewards = copy.copy(rewards)
                    new_rewards.append((max_clock-clock) * v.reward)
                    nav(v, remaining, clock, rewards=new_rewards, paths=new_paths)
            else:
                score = sum(rewards)
                if score > best:
                    print(f"found new best", [valve.name for path in paths for valve in path])
                    best = score
    start = valves[0]
    nav(start ,copy.copy(valves_with_reward))
    print(best)