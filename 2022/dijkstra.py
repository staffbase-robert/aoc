#!/usr/bin/env python3

class Node():
    def __init__(self, edge, cost) -> None:
        self.edge = edge
        self.cost = cost

    def fr(self):
        return self.edge[0]

    def at(self):
        return self.edge[1]

    def __repr__(self) -> str:
        return f"Edge from {self.edge[0]} to {self.edge[1]} with cost {self.cost}"

class Dijkstra():
    def __init__(self, nodes, start_point) -> None:
        self.nodes = nodes
        self.current = {"p": start_point, "cost": 0, "path": [start_point]}
        self.costs = {}
        self.visited = set()
        self.i = 0

    def step(self):
        self.i += 1
        for node in self.nodes:
            if node.fr() == self.current["p"]:
                at = node.at()
                candidate = {
                    "p": at,
                    "cost": node.cost + self.current["cost"], 
                    "path": self.current["path"] + [at]
                }
                if at not in self.costs:
                    self.costs[at] = candidate
                elif self.costs[at]["cost"] > candidate["cost"]:
                    self.costs[at] = candidate
        self.visited.add(self.current["p"])

        # pick next
        potential_visits = list(filter(lambda x: self.costs[x]["p"] not in self.visited, self.costs))
        if len(potential_visits) == 0:
            return True
        nxt = min(potential_visits, key=lambda x: self.costs[x]["cost"])
        self.current = self.costs[nxt]
        return False

    def solve(self):
        while not self.step():
            pass
    def __repr__(self) -> str:
        parts = [f"{k} -> {self.costs[k]['path']} ({self.costs[k]['cost']})" for k in self.costs]
        return f"\nstep {self.i}\n" + "\n".join(parts)


if __name__ == '__main__':
    edges = {
        ("A", "B"): 12, 
        ("A", "E"): 2, 
        ("A", "D"): 4, 
        ("A", "F"): 30, 
        ("E", "B"): 8, 
        ("E", "D"): 1, 
        ("E", "C"): 8,
        ("C", "G"): 12, 
        ("C", "F"): 3, 
        ("G", "B"): 4, 
        ("G", "H"): 5, 
        ("H", "B"): 2, 
    }

    nodes = [Node(edge, edges[edge]) for edge in edges]
    for node in nodes:
        print(node)

    d = Dijkstra(nodes, "A")
    while True:
        if d.step():
            break
        print(d)