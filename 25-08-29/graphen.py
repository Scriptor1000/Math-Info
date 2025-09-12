"""
Graph Theory Implementation

This module provides classes and algorithms for working with directed graphs.
It includes implementations for:
- Basic graph operations (vertex and edge management)
- Graph property checks (reflexive, symmetric, antisymmetric, transitive)
- Eulerian circle detection and finding
- Hamiltonian circle detection and finding

Classes:
    Vertex: Represents a vertex in a graph
    Graph: Represents a directed graph with various algorithms

Author: Math-Informatics Course
Date: 2025-08-29
"""

from dataclasses import dataclass
import itertools


class Vertex:
    """
    Represents a vertex (node) in a graph.
    
    A vertex is identified by a unique string ID and can be used as a key in dictionaries
    due to its implementation of __hash__ and __eq__ methods.
    
    Attributes:
        id (str): The unique identifier for this vertex.
    """
    def __init__(self, id: str):
        """
        Initialize a new vertex with the given ID.
        
        Args:
            id (str): The unique identifier for this vertex.
        """
        self.id = id

    def __eq__(self, other):
        """Check if two vertices are equal based on their IDs."""
        return self.id == other.id

    def __hash__(self):
        """Return hash value for this vertex based on its ID."""
        return hash(self.id)

    def __str__(self):
        """Return string representation of the vertex."""
        return self.id

class Graph:
    """
    Represents a directed graph with vertices and edges.
    
    The graph is implemented as an adjacency list where each vertex maps to a list
    of vertices it has edges to. This implementation supports various graph algorithms
    and property checks.
    
    Attributes:
        _graph (dict[Vertex, list[Vertex]]): Internal adjacency list representation.
    """
    def __init__(self, graph: dict[Vertex, list[Vertex]] = None):
        """
        Initialize a new graph.
        
        Args:
            graph (dict[Vertex, list[Vertex]], optional): Initial adjacency list.
                Defaults to empty graph if None.
        """
        self._graph = graph if graph is not None else {}

    def exist_vertex(self, vertex) -> bool:
        """
        Check if a vertex exists in the graph.
        
        Args:
            vertex (Vertex): The vertex to check for existence.
            
        Returns:
            bool: True if vertex exists in the graph, False otherwise.
        """
        return vertex in self._graph

    def exist_edge(self, start_vertex, end_vertex) -> bool:
        """
        Check if an edge exists between two vertices.
        
        Args:
            start_vertex (Vertex): The source vertex of the edge.
            end_vertex (Vertex): The target vertex of the edge.
            
        Returns:
            bool: True if edge exists, False otherwise.
        """
        return end_vertex in self._graph[start_vertex]

    def get_all_edges(self, vertex) -> list[Vertex]:
        """
        Get all vertices that the given vertex has edges to.
        
        Args:
            vertex (Vertex): The vertex to get edges from.
            
        Returns:
            list[Vertex]: List of vertices that are targets of edges from the given vertex.
        """
        return self._graph[vertex]

    def get_degree(self, vertex) -> int:
        """
        Get the total degree of a vertex (in-degree + out-degree).
        
        For directed graphs, this counts both incoming and outgoing edges.
        Self-loops are counted twice (once as incoming, once as outgoing).
        
        Args:
            vertex (Vertex): The vertex to calculate degree for.
            
        Returns:
            int: The total degree of the vertex.
        """
        # Out-degree: number of edges going out from this vertex
        out_degree = len(self._graph[vertex])
        
        # In-degree: number of edges coming into this vertex from other vertices
        in_degree = sum(1 for other_vertex, targets in self._graph.items() 
                       for target in targets if target == vertex)
        
        return out_degree + in_degree

    def is_reflexive(self) -> bool:
        """
        Check if the graph is reflexive.
        
        A graph is reflexive if every vertex has an edge to itself.
        
        Returns:
            bool: True if the graph is reflexive, False otherwise.
        """
        return all(vertex in vertices for vertex, vertices in self._graph.items())

    def is_symmetric(self) -> bool:
        """
        Check if the graph is symmetric.
        
        A graph is symmetric if for every edge (u,v), there exists an edge (v,u).
        
        Returns:
            bool: True if the graph is symmetric, False otherwise.
        """
        return all(vertex in self._graph[target] for vertex, vertices in self._graph.items() for target in vertices)

    def is_antisymmetric(self) -> bool:
        """
        Check if the graph is antisymmetric.
        
        A graph is antisymmetric if for every edge (u,v) where u≠v, 
        there is no edge (v,u).
        
        Returns:
            bool: True if the graph is antisymmetric, False otherwise.
        """
        return all(target == vertex or vertex not in self._graph[target] for vertex, vertices in self._graph.items() for target in vertices)

    def is_transitive(self) -> bool:
        """
        Check if the graph is transitive.
        
        A graph is transitive if for every path u->v->w, there exists a direct edge u->w.
        
        Returns:
            bool: True if the graph is transitive, False otherwise.
        """
        return all(t_target in vertices for vertex, vertices in self._graph.items() for target in vertices for t_target in self._graph[target])

    def has_euler_circle(self) -> bool:
        """
        Check if the graph has an Eulerian circle.
        
        A graph has an Eulerian circle if it's connected and every vertex has even degree.
        
        Returns:
            bool: True if the graph has an Eulerian circle, False otherwise.
        """
        return all(self.get_degree(v) % 2 == 0 for v in self._graph)

    def find_euler_circle(self):
        """
        Find an Eulerian circle in the graph using Hierholzer's algorithm.
        
        Returns:
            list[Vertex]: A list representing the Eulerian circle, or empty list if none exists.
        """
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
        """
        Find a Hamiltonian circle in the graph using brute force.
        
        A Hamiltonian circle visits every vertex exactly once and returns to the start.
        This implementation uses a brute force approach checking all permutations.
        
        Returns:
            tuple: A tuple representing the Hamiltonian circle, or empty list if none exists.
        """
        vertexes = list(self._graph.keys())
        for permutation in itertools.permutations(vertexes):
            if all(permutation[i+1] in self._graph[permutation[i]] for i in range(len(vertexes)-1)) and permutation[0] in self._graph[permutation[-1]]:
                return permutation
        return []

    def __str__(self):
        """
        Return string representation of the graph as an adjacency list.
        
        Returns:
            str: String representation showing each vertex and its adjacent vertices.
        """
        s = ""
        for k, v in self._graph.items():
            s += f"{k}: {list(map(str, v))}\n"
        return s[:-1]

def main():
    """
    Demonstrate graph algorithms with example graphs.
    
    This function creates two example graphs and demonstrates:
    - Eulerian circle finding
    - Hamiltonian circle finding
    """
    print("=== Graph Theory Demonstration ===\n")
    
    # Create vertices for first example
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")
    f = Vertex("F")
    g = Vertex("G")
    h = Vertex("H")
    i = Vertex("I")

    # Example 1: Smaller graph
    print("Example 1: First Graph")
    k = Graph({a: [f], b: [a,d], c: [b], d: [e,c], e: [f], f: [b, d]})
    print(f"Graph structure:\n{k}")
    
    euler_circle = k.find_euler_circle()
    hamilton_circle = k.find_hamilton_circle()
    
    print(f"Euler circle: {list(map(str, euler_circle))}")
    print(f"Hamilton circle: {hamilton_circle}")
    print(f"Has Euler circle: {k.has_euler_circle()}")
    print()

    # Example 2: Larger graph  
    print("Example 2: Larger Graph")
    g = Graph({a: [i, e, f], b: [a, c], c: [e, i], d: [b, c], e: [d, f], f: [g, a, d], g: [h], h: [f, a], i: [h, b]})
    print(f"Graph structure:\n{g}")
    
    euler_circle = g.find_euler_circle()
    hamilton_circle = g.find_hamilton_circle()
    
    print(f"Euler circle: {list(map(str, euler_circle))}")
    print(f"Hamilton circle: {hamilton_circle}")
    print(f"Has Euler circle: {g.has_euler_circle()}")


if __name__ == "__main__":
    main()