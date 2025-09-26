from dataclasses import dataclass
import itertools


class Vertex:
    def __init__(self, id: str):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return self.id

class Graph:
    def __init__(self, graph: dict[Vertex, list[Vertex]] = None):
        self._graph = graph if graph is not None else {}

    def exist_vertex(self, vertex) -> bool:
        return vertex in self._graph

    def exist_edge(self, start_vertex, end_vertex) -> bool:
        return end_vertex in self._graph[start_vertex]

    def get_all_edges(self, vertex) -> list[Vertex]:
        return self._graph[vertex]

    def get_degree(self, vertex) -> int:
        return len(self._graph[vertex]) + sum(targets.count(vertex) for targets in self._graph.values())

    def is_reflexive(self) -> bool:
        return all(vertex in vertices for vertex, vertices in self._graph.items())

    def is_symmetric(self) -> bool:
        return all(vertex in self._graph[target] for vertex, vertices in self._graph.items() for target in vertices)

    def is_antisymmetric(self) -> bool:
        return all(target == vertex or vertex not in self._graph[target] for vertex, vertices in self._graph.items() for target in vertices)

    def is_transitiv(self) -> bool:
        return all(t_target in vertices for vertex, vertices in self._graph.items() for target in vertices for t_target in self._graph[target])

    def has_euler_circle(self) -> bool:
        return all(self.get_degree(v) % 2 == 0 for v in self._graph)

    def find_euler_circle(self):
        if not self.has_euler_circle():
            return []
        solution = []
        stack = []
        graph = {k: v.copy() for k, v in self._graph.items()}

        start_vertex = list(graph.keys())[0]
        stack.append(start_vertex)

        while stack:
            vertex = stack[-1]
            if vertices := graph[vertex]:
                next_vertex = vertices.pop()
                stack.append(next_vertex)
            else:
                solution.append(stack.pop())
        return solution[::-1]

    def find_hamilton_circle(self):
        vertexes = list(self._graph.keys())
        for permutation in itertools.permutations(vertexes):
            if all(permutation[i+1] in self._graph[permutation[i]] for i in range(len(vertexes)-1)) and permutation[0] in self._graph[permutation[-1]]:
                return permutation
        return []

    def is_connected(self):
        reachable: dict[Vertex, set[Vertex]] = {v: set([v]) for v in self._graph}

        for start_vertex in self._graph:
            adjacent_vertexes: set[Vertex] = set()
            adjacent_vertexes.update(self._graph[start_vertex])
            while adjacent_vertexes:
                current_vertex = adjacent_vertexes.pop()
                reachable[start_vertex].add(current_vertex)
                reachable[start_vertex].update(reachable[current_vertex])
                if len(reachable[start_vertex]) == len(self._graph):
                    break
                for next_vertex in self._graph[current_vertex]:
                    if next_vertex not in reachable[start_vertex]:
                        adjacent_vertexes.add(next_vertex)
            if len(reachable[start_vertex]) != len(self._graph):
                return False
        return True

    def __str__(self):
        s = ""
        for k, v in self._graph.items():
            s += f"{k}: {list(map(str, v))}\n"
        return s[:-1]

if __name__ == "__main__":
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")
    f = Vertex("F")
    g = Vertex("G")
    h = Vertex("H")
    i = Vertex("I")

    l = Graph({a: [c], b: [c], c: [d], d: [a]})
    print(l.is_connected())

    m = Graph({a: [f, e], b: [a], c: [b], d: [a], e: [f], f: [b, c, d]})
    print(m.is_connected())

    k = Graph({a: [f], b: [a,d], c: [b], d: [e,c], e: [f], f: [b, d]})
    print(list(map(str, k.find_euler_circle())))
    print(k.find_hamilton_circle())

    g = Graph({a: [i, e, f], b: [a, c], c: [e, i], d: [b, c], e: [d, f], f: [g, a, d], g: [h], h: [f, a], i: [h, b]})
    print(list(map(str, g.find_euler_circle())))
    print(g.find_hamilton_circle())