from dataclasses import dataclass
import pprint


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

    k = Graph({a: [f], b: [a,d], c: [b], d: [e,c], e: [f], f: [b, d]})
    print(list(map(str, k.find_euler_circle())))

    g = Graph({a: [i, e, f], b: [a, c], c: [e, i], d: [b, c], e: [d, f], f: [g, a, d], g: [h], h: [f, a], i: [h, b]})
    print(list(map(str, g.find_euler_circle())))