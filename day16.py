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
    def __init__(self, name, flowrate, doors, ) -> None:
        self.name = name
        self.flowrate = flowrate
        self.doors = doors
        self.connections = None

    def connect(self, all_valves):
        self.connections = [(find_by_name(all_valves, door), 1) for door in self.doors]

    def __repr__(self) -> str:
        return f"{self.name}: flowrate: {self.flowrate}, doors: {self.doors}"

import graphviz

def visualize(valve):
    e = graphviz.Graph('ER', filename='er.gv', engine='neato')
    def draw_edges(valve, visited = set()):
        visited.add(valve)
        e.node(valve.name, label=f"{valve.name} - {valve.flowrate}")
        for con, cost in valve.connections:
            e.edge(valve.name, con.name, label=f"{cost}", len="3")

        for con, _ in valve.connections:
            if con not in visited:
                draw_edges(con, visited=visited)

    draw_edges(valve)
    return e

with open("input-16") as f:
    IN = f.read()
    # IN = example
    valves = [Valve(match[0], int(match[1]), match[2].split(', ')) for match in re.findall(r"Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? (.*)", IN, re.MULTILINE)]
    for valve in valves:
        valve.connect(valves)

    # visualize(valves[0]).view()
    rewards = list(filter(lambda v: v.flowrate > 0, valves))
    rewards = sorted(rewards, key=lambda v: v.flowrate, reverse=True)
    for v in rewards:
        print(v)


    cache = {}
    def find_routes(v, target):
        key = (v, target)
        if key in cache:
            return cache[key]

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
        cache[key] = routes
        return routes

    max_clock = 30
    best = -1
    def nav(current, targets, minute=0, rewards=[], order_of_opens=[]):
        global best

        if len(targets) == 0 or minute <= max_clock:
            score = sum([r[0] * (max_clock - r[1]) for r in rewards])
            if score > best:
                print(f"found new best {score},\nrewards={', '.join([str(r) for r in rewards])}")
                best = score

        for vi in range(len(targets)):
            v = targets[vi]
            routes = find_routes(current, v)
            shortest = min(routes, key=lambda r: len(r))
            remaining = targets[0:vi] + targets[vi+1:]
            clock = minute + len(shortest) + 1

            new_order_of_opens = copy.copy(order_of_opens)
            new_order_of_opens.append((v.name, v.flowrate))
            new_rewards = copy.copy(rewards)
            new_rewards.append([v.flowrate, clock, v.name])
            if len(remaining) >= 0:
                if clock <= max_clock:
                    # print(f"--- reached new reward in minute={clock} - collecting {reward} reward ---")
                    nav(v, remaining, clock, rewards=new_rewards, order_of_opens=new_order_of_opens)
        
    start = find_by_name(valves, "AA")
    nav(start ,copy.copy(rewards))
    print(best)