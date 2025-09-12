#!/usr/bin/env python3
"""
Simple tests for the graph implementation to validate functionality
before and after improvements.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '25-08-29'))

from graphen import Vertex, Graph


def test_vertex_creation():
    """Test vertex creation and equality."""
    v1 = Vertex("A")
    v2 = Vertex("A")
    v3 = Vertex("B")
    
    assert v1 == v2, "Vertices with same id should be equal"
    assert v1 != v3, "Vertices with different ids should not be equal"
    assert str(v1) == "A", "String representation should match id"
    print("✅ Vertex creation tests passed")


def test_graph_basic_operations():
    """Test basic graph operations."""
    a = Vertex("A")
    b = Vertex("B") 
    c = Vertex("C")
    
    # Create a simple graph: A -> B -> C
    graph = Graph({a: [b], b: [c], c: []})
    
    assert graph.exist_vertex(a), "Vertex A should exist"
    assert graph.exist_vertex(b), "Vertex B should exist"  
    assert graph.exist_vertex(c), "Vertex C should exist"
    
    assert graph.exist_edge(a, b), "Edge A->B should exist"
    assert graph.exist_edge(b, c), "Edge B->C should exist"
    assert not graph.exist_edge(c, a), "Edge C->A should not exist"
    
    print("✅ Graph basic operations tests passed")


def test_graph_properties():
    """Test graph property detection."""
    a = Vertex("A")
    b = Vertex("B")
    
    # Test reflexive graph: A->A, B->B
    reflexive_graph = Graph({a: [a], b: [b]})
    assert reflexive_graph.is_reflexive(), "Should be reflexive"
    
    # Test symmetric graph: A->B, B->A
    symmetric_graph = Graph({a: [b], b: [a]})
    assert symmetric_graph.is_symmetric(), "Should be symmetric"
    
    print("✅ Graph properties tests passed")


def test_current_examples():
    """Test the examples from the main section."""
    a = Vertex("A")
    b = Vertex("B")
    c = Vertex("C")
    d = Vertex("D")
    e = Vertex("E")
    f = Vertex("F")
    
    # Test first graph from main
    k = Graph({a: [f], b: [a,d], c: [b], d: [e,c], e: [f], f: [b, d]})
    euler_result = k.find_euler_circle()
    hamilton_result = k.find_hamilton_circle()
    
    print(f"✅ First graph Euler circle: {[str(v) for v in euler_result]}")
    print(f"✅ First graph Hamilton circle: {hamilton_result}")
    
    # Test graph properties work without errors
    k.is_reflexive()
    k.is_symmetric() 
    k.is_antisymmetric()
    k.is_transitive()  # Note: now using corrected method name
    
    print("✅ Current examples tests passed")


if __name__ == "__main__":
    print("Running tests for graph implementation...")
    test_vertex_creation()
    test_graph_basic_operations()
    test_graph_properties()
    test_current_examples()
    print("\n🎉 All tests passed! Current functionality is preserved.")