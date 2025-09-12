#!/usr/bin/env python3
"""
Unit tests for Graph.get_degree() method.

Tests degree calculation (in-degree + out-degree) for vertices in various graph configurations.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestGetDegree:
    """Test Graph.get_degree() method."""
    
    def test_get_degree_empty_graph(self):
        """Test get_degree on empty graph."""
        graph = Graph()
        vertex_a = Vertex("A")
        
        # Should raise KeyError for non-existent vertex
        with pytest.raises(KeyError):
            graph.get_degree(vertex_a)
    
    def test_get_degree_single_vertex_no_edges(self):
        """Test get_degree with single isolated vertex."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        degree = graph.get_degree(vertex_a)
        assert degree == 0
    
    def test_get_degree_single_vertex_self_loop(self):
        """Test get_degree with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        # Self-loop counts as both in-degree and out-degree: 1 + 1 = 2
        degree = graph.get_degree(vertex_a)
        assert degree == 2
    
    def test_get_degree_single_vertex_multiple_self_loops(self):
        """Test get_degree with single vertex having multiple self-loops."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a, vertex_a, vertex_a]})
        
        # Multiple self-loops: out-degree=3, in-degree=3, total=6
        degree = graph.get_degree(vertex_a)
        assert degree == 6
    
    def test_get_degree_simple_chain(self):
        """Test get_degree with simple chain A -> B -> C."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A: out=1, in=0
            vertex_b: [vertex_c],  # B: out=1, in=1
            vertex_c: []           # C: out=0, in=1
        })
        
        assert graph.get_degree(vertex_a) == 1  # out=1, in=0
        assert graph.get_degree(vertex_b) == 2  # out=1, in=1
        assert graph.get_degree(vertex_c) == 1  # out=0, in=1
    
    def test_get_degree_simple_cycle(self):
        """Test get_degree with simple cycle A -> B -> C -> A."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A: out=1, in=1 (from C)
            vertex_b: [vertex_c],  # B: out=1, in=1 (from A)
            vertex_c: [vertex_a]   # C: out=1, in=1 (from B)
        })
        
        # In a cycle, each vertex has degree 2
        assert graph.get_degree(vertex_a) == 2
        assert graph.get_degree(vertex_b) == 2
        assert graph.get_degree(vertex_c) == 2
    
    def test_get_degree_star_graph_center(self):
        """Test get_degree for center vertex in star graph."""
        vertex_center = Vertex("Center")
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_center: [vertex_a, vertex_b, vertex_c],  # Center: out=3, in=0
            vertex_a: [],                                   # A: out=0, in=1
            vertex_b: [],                                   # B: out=0, in=1
            vertex_c: []                                    # C: out=0, in=1
        })
        
        assert graph.get_degree(vertex_center) == 3  # out=3, in=0
        assert graph.get_degree(vertex_a) == 1       # out=0, in=1
        assert graph.get_degree(vertex_b) == 1       # out=0, in=1
        assert graph.get_degree(vertex_c) == 1       # out=0, in=1
    
    def test_get_degree_star_graph_bidirectional(self):
        """Test get_degree for center vertex in bidirectional star graph."""
        vertex_center = Vertex("Center")
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_center: [vertex_a, vertex_b, vertex_c],  # Center: out=3, in=3
            vertex_a: [vertex_center],                      # A: out=1, in=1
            vertex_b: [vertex_center],                      # B: out=1, in=1
            vertex_c: [vertex_center]                       # C: out=1, in=1
        })
        
        assert graph.get_degree(vertex_center) == 6  # out=3, in=3
        assert graph.get_degree(vertex_a) == 2       # out=1, in=1
        assert graph.get_degree(vertex_b) == 2       # out=1, in=1
        assert graph.get_degree(vertex_c) == 2       # out=1, in=1
    
    def test_get_degree_complete_graph_3(self):
        """Test get_degree with complete graph of 3 vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A: out=2, in=2 (from B,C)
            vertex_b: [vertex_a, vertex_c],  # B: out=2, in=2 (from A,C)
            vertex_c: [vertex_a, vertex_b]   # C: out=2, in=2 (from A,B)
        })
        
        # In complete graph, each vertex has same degree
        assert graph.get_degree(vertex_a) == 4
        assert graph.get_degree(vertex_b) == 4
        assert graph.get_degree(vertex_c) == 4
    
    def test_get_degree_with_multiple_edges_same_target(self):
        """Test get_degree when vertex has multiple edges to same target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],  # A: out=3, in=0
            vertex_b: []                               # B: out=0, in=3
        })
        
        assert graph.get_degree(vertex_a) == 3  # out=3, in=0
        assert graph.get_degree(vertex_b) == 3  # out=0, in=3
    
    def test_get_degree_mixed_self_loops_and_others(self):
        """Test get_degree with mix of self-loops and other edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_a],  # A: out=3, in=2 (self-loops)
            vertex_b: [vertex_b]                       # B: out=1, in=2 (self+from A)
        })
        
        assert graph.get_degree(vertex_a) == 5  # out=3, in=2
        assert graph.get_degree(vertex_b) == 3  # out=1, in=2
    
    def test_get_degree_disconnected_components(self):
        """Test get_degree with disconnected graph components."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],  # Component 1: A->B
            vertex_b: [vertex_a],  # Component 1: B->A
            vertex_c: [vertex_d],  # Component 2: C->D
            vertex_d: []           # Component 2: isolated end
        })
        
        assert graph.get_degree(vertex_a) == 2  # out=1, in=1
        assert graph.get_degree(vertex_b) == 2  # out=1, in=1
        assert graph.get_degree(vertex_c) == 1  # out=1, in=0
        assert graph.get_degree(vertex_d) == 1  # out=0, in=1
    
    def test_get_degree_vertex_only_as_target(self):
        """Test get_degree when vertex exists only as edge target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b appears only as target, not as key
        graph = Graph({vertex_a: [vertex_b]})
        
        # Should raise KeyError because vertex_b is not a key in the graph
        with pytest.raises(KeyError):
            graph.get_degree(vertex_b)


class TestGetDegreeErrorCases:
    """Test error cases for get_degree method."""
    
    def test_get_degree_vertex_not_exists(self):
        """Test get_degree when vertex doesn't exist in graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.get_degree(vertex_b)
    
    def test_get_degree_with_none(self):
        """Test get_degree behavior when passed None."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.get_degree(None)
    
    def test_get_degree_with_non_vertex_object(self):
        """Test get_degree behavior with non-Vertex object."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.get_degree("A")


class TestGetDegreeSpecialCases:
    """Test special cases for get_degree method."""
    
    def test_get_degree_same_id_different_object(self):
        """Test get_degree with vertex having same ID but different object."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a1: [vertex_b],
            vertex_b: [vertex_a1]
        })
        
        # Should work because vertices are equal based on ID
        degree1 = graph.get_degree(vertex_a1)
        degree2 = graph.get_degree(vertex_a2)
        
        assert degree1 == 2  # out=1, in=1
        assert degree2 == 2  # out=1, in=1
        assert degree1 == degree2
    
    def test_get_degree_empty_string_vertices(self):
        """Test get_degree with vertices having empty string IDs."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty: [vertex_a],
            vertex_a: [vertex_empty]
        })
        
        degree_empty = graph.get_degree(vertex_empty)
        degree_a = graph.get_degree(vertex_a)
        
        assert degree_empty == 2  # out=1, in=1
        assert degree_a == 2      # out=1, in=1
    
    def test_get_degree_special_character_vertices(self):
        """Test get_degree with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_unicode],
            vertex_unicode: [vertex_whitespace],
            vertex_whitespace: [vertex_special]
        })
        
        assert graph.get_degree(vertex_special) == 2    # out=1, in=1
        assert graph.get_degree(vertex_unicode) == 2    # out=1, in=1
        assert graph.get_degree(vertex_whitespace) == 2 # out=1, in=1
    
    def test_get_degree_return_type(self):
        """Test that get_degree always returns an integer."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Test various degree values
        test_cases = [
            ({vertex_a: []}, vertex_a, 0),                          # Isolated vertex
            ({vertex_a: [vertex_a]}, vertex_a, 2),                  # Self-loop
            ({vertex_a: [vertex_b], vertex_b: []}, vertex_a, 1),    # Out-edge only
            ({vertex_a: [], vertex_b: [vertex_a]}, vertex_a, 1),    # In-edge only
            ({vertex_a: [vertex_b], vertex_b: [vertex_a]}, vertex_a, 2)  # Bidirectional
        ]
        
        for graph_data, vertex, expected_degree in test_cases:
            graph = Graph(graph_data)
            degree = graph.get_degree(vertex)
            assert isinstance(degree, int)
            assert degree == expected_degree
    
    def test_get_degree_large_graph(self):
        """Test get_degree performance with large graph."""
        vertices = [Vertex(str(i)) for i in range(100)]
        
        # Create complete graph (every vertex connects to every other)
        graph_data = {}
        for i in range(100):
            graph_data[vertices[i]] = [v for j, v in enumerate(vertices) if i != j]
        
        graph = Graph(graph_data)
        
        # In complete graph with n vertices, each vertex has degree 2*(n-1)
        # out-degree = n-1, in-degree = n-1
        for vertex in vertices[:10]:  # Test first 10 vertices
            degree = graph.get_degree(vertex)
            assert degree == 2 * 99  # 2 * (100-1)
    
    def test_get_degree_algorithmic_correctness(self):
        """Test algorithmic correctness of degree calculation."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # Create specific test case
        graph = Graph({
            vertex_a: [vertex_b, vertex_c, vertex_a],  # A->B, A->C, A->A
            vertex_b: [vertex_a],                      # B->A
            vertex_c: [vertex_a, vertex_a]             # C->A, C->A
        })
        
        # Manual calculation for vertex_a:
        # Out-degree: 3 (to B, C, A)
        # In-degree: 1 (from B) + 2 (from C) + 1 (self-loop) = 4
        # Total: 3 + 4 = 7
        assert graph.get_degree(vertex_a) == 7
        
        # Manual calculation for vertex_b:
        # Out-degree: 1 (to A)
        # In-degree: 1 (from A)
        # Total: 1 + 1 = 2
        assert graph.get_degree(vertex_b) == 2
        
        # Manual calculation for vertex_c:
        # Out-degree: 2 (to A, A)
        # In-degree: 1 (from A)
        # Total: 2 + 1 = 3
        assert graph.get_degree(vertex_c) == 3
    
    def test_get_degree_consistency(self):
        """Test that get_degree results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_a],
            vertex_b: [vertex_a]
        })
        
        # Multiple calls should return same result
        for _ in range(5):
            assert graph.get_degree(vertex_a) == 4  # out=2, in=2
            assert graph.get_degree(vertex_b) == 2  # out=1, in=1