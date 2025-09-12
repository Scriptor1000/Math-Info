#!/usr/bin/env python3
"""
Unit tests for Graph.is_symmetric() method.

Tests symmetry checking: a graph is symmetric if for every edge (u,v), there exists an edge (v,u).
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestIsSymmetric:
    """Test Graph.is_symmetric() method."""
    
    def test_is_symmetric_empty_graph(self):
        """Test is_symmetric on empty graph."""
        graph = Graph()
        
        # Empty graph is vacuously symmetric (no edges to violate symmetry)
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_single_vertex_no_edges(self):
        """Test is_symmetric with single vertex having no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # No edges means symmetric
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_single_vertex_self_loop(self):
        """Test is_symmetric with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        # Self-loop is symmetric by definition (A->A implies A->A)
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_two_vertices_bidirectional(self):
        """Test is_symmetric with bidirectional edge between two vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: [vertex_a]   # B -> A (symmetric)
        })
        
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_two_vertices_unidirectional(self):
        """Test is_symmetric with unidirectional edge between two vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: []           # No B -> A (not symmetric)
        })
        
        assert graph.is_symmetric() == False
    
    def test_is_symmetric_triangle_all_bidirectional(self):
        """Test is_symmetric with triangle where all edges are bidirectional."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A -> B, A -> C
            vertex_b: [vertex_a, vertex_c],  # B -> A, B -> C
            vertex_c: [vertex_a, vertex_b]   # C -> A, C -> B
        })
        
        # All edges are bidirectional, so symmetric
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_triangle_one_unidirectional(self):
        """Test is_symmetric with triangle where one edge is unidirectional."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A -> B, A -> C
            vertex_b: [vertex_a],            # B -> A (missing B -> C)
            vertex_c: [vertex_a, vertex_b]   # C -> A, C -> B
        })
        
        # B -> C exists but C -> B doesn't exist bidirectionally (B doesn't have edge to C)
        # Wait, let me reconsider: A->C exists, C->A exists (good)
        # A->B exists, B->A exists (good)
        # C->B exists, but B->C doesn't exist (bad)
        assert graph.is_symmetric() == False
    
    def test_is_symmetric_cycle_graph(self):
        """Test is_symmetric with cycle graph A -> B -> C -> A."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: [vertex_c],  # B -> C
            vertex_c: [vertex_a]   # C -> A
        })
        
        # A->B exists but B->A doesn't, so not symmetric
        assert graph.is_symmetric() == False
    
    def test_is_symmetric_complete_graph(self):
        """Test is_symmetric with complete graph (all possible edges)."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        })
        
        # Complete graph is symmetric
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_with_self_loops_and_bidirectional(self):
        """Test is_symmetric with mix of self-loops and bidirectional edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A -> A, A -> B
            vertex_b: [vertex_b, vertex_a]   # B -> B, B -> A
        })
        
        # Both self-loops and bidirectional edge, so symmetric
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_with_multiple_edges_same_direction(self):
        """Test is_symmetric with multiple edges in same direction."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b],  # A -> B (twice)
            vertex_b: [vertex_a]             # B -> A (once)
        })
        
        # A->B exists and B->A exists, so symmetric (multiplicity doesn't matter for symmetry)
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_disconnected_components_all_symmetric(self):
        """Test is_symmetric with disconnected components, all symmetric."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],  # Component 1: A <-> B
            vertex_b: [vertex_a],
            vertex_c: [vertex_d],  # Component 2: C <-> D
            vertex_d: [vertex_c]
        })
        
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_disconnected_components_mixed(self):
        """Test is_symmetric with disconnected components, mixed symmetry."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],  # Component 1: A <-> B (symmetric)
            vertex_b: [vertex_a],
            vertex_c: [vertex_d],  # Component 2: C -> D (not symmetric)
            vertex_d: []
        })
        
        assert graph.is_symmetric() == False
    
    def test_is_symmetric_isolated_vertices(self):
        """Test is_symmetric with isolated vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [],  # Isolated
            vertex_b: [],  # Isolated
            vertex_c: []   # Isolated
        })
        
        # No edges means symmetric
        assert graph.is_symmetric() == True


class TestIsSymmetricErrorCases:
    """Test error cases for is_symmetric method."""
    
    def test_is_symmetric_vertex_only_as_target(self):
        """Test is_symmetric when vertex appears only as edge target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b appears only as target, not as key in graph
        graph = Graph({vertex_a: [vertex_b]})
        
        # The current implementation should handle this correctly
        # A->B exists, but B is not a key so B->A cannot exist
        # This should make the graph non-symmetric
        assert graph.is_symmetric() == False


class TestIsSymmetricSpecialCases:
    """Test special cases for is_symmetric method."""
    
    def test_is_symmetric_empty_string_vertices(self):
        """Test is_symmetric with vertices having empty string IDs."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty: [vertex_a],
            vertex_a: [vertex_empty]
        })
        
        assert graph.is_symmetric() == True
        
        # Test non-symmetric case
        graph2 = Graph({
            vertex_empty: [vertex_a],
            vertex_a: []  # Missing reverse edge
        })
        
        assert graph2.is_symmetric() == False
    
    def test_is_symmetric_special_character_vertices(self):
        """Test is_symmetric with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_unicode],
            vertex_unicode: [vertex_whitespace],
            vertex_whitespace: [vertex_special]
        })
        
        # Not symmetric (no reverse edges)
        assert graph.is_symmetric() == False
        
        # Make it symmetric
        graph_symmetric = Graph({
            vertex_special: [vertex_unicode],
            vertex_unicode: [vertex_special, vertex_whitespace],
            vertex_whitespace: [vertex_unicode]
        })
        
        assert graph_symmetric.is_symmetric() == True
    
    def test_is_symmetric_same_id_different_objects(self):
        """Test is_symmetric with vertices having same ID but different objects."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a1: [vertex_b],
            vertex_b: [vertex_a2]  # Should be treated as edge to same vertex as vertex_a1
        })
        
        # Should be symmetric because vertex_a1 and vertex_a2 are considered equal
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_large_graph_symmetric(self):
        """Test is_symmetric performance with large symmetric graph."""
        vertices = [Vertex(str(i)) for i in range(50)]
        
        # Create symmetric graph: each vertex connects to its neighbors in both directions
        graph_data = {}
        for i, vertex in enumerate(vertices):
            neighbors = []
            for j in range(max(0, i-2), min(len(vertices), i+3)):
                if i != j:  # Don't include self
                    neighbors.append(vertices[j])
            graph_data[vertex] = neighbors
        
        graph = Graph(graph_data)
        assert graph.is_symmetric() == True
    
    def test_is_symmetric_large_graph_non_symmetric(self):
        """Test is_symmetric performance with large non-symmetric graph."""
        vertices = [Vertex(str(i)) for i in range(50)]
        
        # Create non-symmetric graph: directed chain
        graph_data = {}
        for i, vertex in enumerate(vertices):
            if i < len(vertices) - 1:
                graph_data[vertex] = [vertices[i + 1]]
            else:
                graph_data[vertex] = []
        
        graph = Graph(graph_data)
        assert graph.is_symmetric() == False
    
    def test_is_symmetric_consistency(self):
        """Test that is_symmetric results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Symmetric graph
        graph1 = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_a]
        })
        
        # Non-symmetric graph
        graph2 = Graph({
            vertex_a: [vertex_b],
            vertex_b: []
        })
        
        # Multiple calls should return same result
        for _ in range(5):
            assert graph1.is_symmetric() == True
            assert graph2.is_symmetric() == False
    
    def test_is_symmetric_return_type(self):
        """Test that is_symmetric always returns a boolean."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        test_cases = [
            Graph(),                                        # Empty
            Graph({vertex_a: []}),                         # Single vertex, no edges
            Graph({vertex_a: [vertex_b], vertex_b: []}),   # Non-symmetric
            Graph({vertex_a: [vertex_b], vertex_b: [vertex_a]})  # Symmetric
        ]
        
        for graph in test_cases:
            result = graph.is_symmetric()
            assert isinstance(result, bool)
    
    def test_is_symmetric_algorithm_correctness(self):
        """Test the algorithmic correctness of symmetry check."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # Test complex case
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],     # A -> B, A -> C
            vertex_b: [vertex_a],               # B -> A (A->B is symmetric)
            vertex_c: [vertex_b]                # C -> B (A->C is NOT symmetric, C->B needs B->C)
        })
        
        # Manual check:
        # A->B: need B->A? Yes, exists. OK.
        # A->C: need C->A? No, doesn't exist. NOT OK.
        # B->A: need A->B? Yes, exists. OK.
        # C->B: need B->C? No, doesn't exist. NOT OK.
        # Result: False
        
        assert graph.is_symmetric() == False
        
        # Fix it by adding missing edges
        graph._graph[vertex_c].append(vertex_a)  # Add C->A
        graph._graph[vertex_b].append(vertex_c)  # Add B->C
        
        assert graph.is_symmetric() == True