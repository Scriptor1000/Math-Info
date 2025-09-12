#!/usr/bin/env python3
"""
Advanced demonstration of the graph implementation showing various graph properties
and edge cases.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '25-08-29'))

from graphen import Vertex, Graph


def demonstrate_graph_properties():
    """Demonstrate various graph properties with specific examples."""
    print("=== Graph Properties Demonstration ===\n")
    
    # Create vertices
    a, b, c = Vertex("A"), Vertex("B"), Vertex("C")
    
    # 1. Reflexive graph
    print("1. Reflexive Graph:")
    reflexive_graph = Graph({a: [a, b], b: [b], c: [c]})
    print(f"   Graph: {reflexive_graph}")
    print(f"   Is reflexive: {reflexive_graph.is_reflexive()}")
    print(f"   Is symmetric: {reflexive_graph.is_symmetric()}")
    print()
    
    # 2. Symmetric graph
    print("2. Symmetric Graph:")
    symmetric_graph = Graph({a: [b], b: [a], c: []})
    print(f"   Graph: {symmetric_graph}")
    print(f"   Is symmetric: {symmetric_graph.is_symmetric()}")
    print(f"   Is antisymmetric: {symmetric_graph.is_antisymmetric()}")
    print()
    
    # 3. Antisymmetric graph
    print("3. Antisymmetric Graph:")
    antisymmetric_graph = Graph({a: [b], b: [c], c: []})
    print(f"   Graph: {antisymmetric_graph}")
    print(f"   Is antisymmetric: {antisymmetric_graph.is_antisymmetric()}")
    print(f"   Is transitive: {antisymmetric_graph.is_transitive()}")
    print()
    
    # 4. Transitive graph
    print("4. Transitive Graph:")
    transitive_graph = Graph({a: [b, c], b: [c], c: []})
    print(f"   Graph: {transitive_graph}")
    print(f"   Is transitive: {transitive_graph.is_transitive()}")
    print()


def demonstrate_degree_calculation():
    """Demonstrate degree calculation for different graph types."""
    print("=== Degree Calculation Demonstration ===\n")
    
    a, b, c = Vertex("A"), Vertex("B"), Vertex("C")
    
    # Simple directed graph
    graph = Graph({a: [b, c], b: [c], c: [a]})
    print("Directed Graph:")
    print(f"Graph: {graph}")
    print("Degrees:")
    for vertex in [a, b, c]:
        degree = graph.get_degree(vertex)
        print(f"   Vertex {vertex}: degree = {degree}")
    print()
    
    # Graph with self-loop
    self_loop_graph = Graph({a: [a, b], b: [c], c: []})
    print("Graph with Self-loop:")
    print(f"Graph: {self_loop_graph}")
    print("Degrees:")
    for vertex in [a, b, c]:
        degree = self_loop_graph.get_degree(vertex)
        print(f"   Vertex {vertex}: degree = {degree}")
    print()


def demonstrate_empty_and_edge_cases():
    """Demonstrate behavior with empty graphs and edge cases."""
    print("=== Edge Cases Demonstration ===\n")
    
    # Empty graph
    empty_graph = Graph()
    print("1. Empty Graph:")
    print(f"   Has Euler circle: {empty_graph.has_euler_circle()}")
    print(f"   Euler circle: {empty_graph.find_euler_circle()}")
    print(f"   Hamilton circle: {empty_graph.find_hamilton_circle()}")
    print()
    
    # Single vertex with self-loop
    a = Vertex("A")
    single_vertex = Graph({a: [a]})
    print("2. Single Vertex with Self-loop:")
    print(f"   Graph: {single_vertex}")
    print(f"   Has Euler circle: {single_vertex.has_euler_circle()}")
    print(f"   Euler circle: {list(map(str, single_vertex.find_euler_circle()))}")
    print(f"   Hamilton circle: {single_vertex.find_hamilton_circle()}")
    print()


if __name__ == "__main__":
    demonstrate_graph_properties()
    demonstrate_degree_calculation() 
    demonstrate_empty_and_edge_cases()
    print("=== Demonstration Complete ===")