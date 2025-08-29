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
        return len(self._graph[vertex]) + 1 if vertex in self._graph[vertex] else 0

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
    g = Graph({a: [b], b: [b, c, d], c: [a], d: []})
    print(g)