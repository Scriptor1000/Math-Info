from collections import defaultdict
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

class WeightedGraph(Graph):
    def __init__(self, graph: dict[Vertex, dict[Vertex, int]]):
        self._graph = {k: list(v.keys()) for k, v in graph.items()}
        self.weights = {(k, target): weight for k, v in graph.items() for target, weight in v.items()}

    def find_minimal_spanning_tree(self) -> 'WeightedGraph':
        self.parents = {}
        edges = [(weight, v1, v2) for (v1, v2), weight in self.weights.items()]
        sorted_edges = sorted(edges, key=lambda x: x[0])
        self.mst = []

        for weight, v1, v2 in sorted_edges:
            if not self._creates_cycle(v1, v2):
                self.mst.append((v1, v2, weight))

        _graph = defaultdict(dict)
        for v1, v2, weight in self.mst:
            _graph[v1][v2] = weight
            
        return WeightedGraph(_graph)

    def _creates_cycle(self, v1, v2):
        def find(vertex):
            if self.parents[vertex] != vertex:
                self.parents[vertex] = find(self.parents[vertex])
            return self.parents[vertex]

        def union(v1, v2):
            root1 = find(v1)
            root2 = find(v2)
            if root1 != root2:
                self.parents[root2] = root1


        if v1 not in self.parents:
            self.parents[v1] = v1
        if v2 not in self.parents:
            self.parents[v2] = v2

        if find(v1) == find(v2):
            return True
        
        union(v1, v2)
        return False
        
    
    def find_minimal_spanning_tree_copilot(self):
        """Finds the minimal spanning tree using Kruskal's algorithm. 
        Implemented by pressing Tab to accept Github Copilot's suggestion."""

        parent = {}
        rank = {}

        def find(vertex):
            if parent[vertex] != vertex:
                parent[vertex] = find(parent[vertex])
            return parent[vertex]

        def union(v1, v2):
            root1 = find(v1)
            root2 = find(v2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root1] = root2
                    if rank[root1] == rank[root2]:
                        rank[root2] += 1

        for vertex in self._graph:
            parent[vertex] = vertex
            rank[vertex] = 0

        edges = sorted(self.weights.items(), key=lambda item: item[1])
        mst = []

        for (v1, v2), weight in edges:
            if find(v1) != find(v2):
                union(v1, v2)
                mst.append((v1, v2, weight))

        return mst


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

    g = WeightedGraph({a: {b: 7, d: 5}, b: {a: 7, c: 8, d: 9, e: 7}, c: {b: 8, e: 5}, d: {a: 5, b: 9, e: 15, f: 6}, e: {b: 7, c: 5, d: 15, f: 8}, f: {d: 6, e: 8}})
    mst = g.find_minimal_spanning_tree()
    print(mst)