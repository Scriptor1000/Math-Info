#!/usr/bin/env python3
"""
Unit tests for Graph.is_antisymmetric() method.

Tests antisymmetry checking: a graph is antisymmetric if for every edge (u,v) where u≠v, 
there is no edge (v,u). Self-loops are allowed.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestIsAntisymmetric:
    """Test Graph.is_antisymmetric() method."""
    
    def test_is_antisymmetric_empty_graph(self):
        """Test is_antisymmetric on empty graph."""
        graph = Graph()
        
        # Empty graph is vacuously antisymmetric
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_single_vertex_no_edges(self):
        """Test is_antisymmetric with single vertex having no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # No edges means antisymmetric
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_single_vertex_self_loop(self):
        """Test is_antisymmetric with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        # Self-loops are allowed in antisymmetric graphs
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_two_vertices_unidirectional(self):
        """Test is_antisymmetric with unidirectional edge between two vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: []           # No B -> A (good for antisymmetric)
        })
        
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_two_vertices_bidirectional(self):
        """Test is_antisymmetric with bidirectional edge between two vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: [vertex_a]   # B -> A (violates antisymmetry)
        })
        
        assert graph.is_antisymmetric() == False
    
    def test_is_antisymmetric_directed_acyclic_graph(self):
        """Test is_antisymmetric with directed acyclic graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A -> B, A -> C
            vertex_b: [vertex_c],            # B -> C
            vertex_c: []                     # C has no outgoing edges
        })
        
        # No bidirectional edges, so antisymmetric
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_with_self_loops_only(self):
        """Test is_antisymmetric with only self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a],  # A -> A (self-loop allowed)
            vertex_b: [vertex_b],  # B -> B (self-loop allowed)
            vertex_c: [vertex_c]   # C -> C (self-loop allowed)
        })
        
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_with_cycle(self):
        """Test is_antisymmetric with cycle (should fail)."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: [vertex_c],  # B -> C
            vertex_c: [vertex_a]   # C -> A (creates cycle)
        })
        
        # No direct bidirectional edges, so should be antisymmetric
        # (antisymmetric doesn't prevent cycles, just direct bidirectional edges)
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_mixed_self_loops_and_directed_edges(self):
        """Test is_antisymmetric with mix of self-loops and directed edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A -> A (allowed), A -> B
            vertex_b: [vertex_b, vertex_c],  # B -> B (allowed), B -> C  
            vertex_c: [vertex_c]             # C -> C (allowed)
        })
        
        # Self-loops allowed, no bidirectional edges between different vertices
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_violation_case(self):
        """Test is_antisymmetric with bidirectional edges (violation)."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A -> A, A -> B
            vertex_b: [vertex_b, vertex_a],  # B -> B, B -> A (bidirectional with A)
            vertex_c: [vertex_c]             # C -> C
        })
        
        # A->B and B->A violates antisymmetry
        assert graph.is_antisymmetric() == False
    
    def test_is_antisymmetric_multiple_violations(self):
        """Test is_antisymmetric with multiple bidirectional edge pairs."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A -> B, A -> C
            vertex_b: [vertex_a, vertex_c],  # B -> A (violation), B -> C
            vertex_c: [vertex_a, vertex_b]   # C -> A (violation), C -> B (violation)
        })
        
        # Multiple bidirectional pairs violate antisymmetry
        assert graph.is_antisymmetric() == False
    
    def test_is_antisymmetric_tree_structure(self):
        """Test is_antisymmetric with tree structure."""
        vertex_root = Vertex("Root")
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_root: [vertex_a, vertex_b],  # Root -> A, Root -> B
            vertex_a: [vertex_c],               # A -> C
            vertex_b: [vertex_d],               # B -> D
            vertex_c: [],                       # Leaf
            vertex_d: []                        # Leaf
        })
        
        # Tree structure has no bidirectional edges
        assert graph.is_antisymmetric() == True


class TestIsAntisymmetricSpecialCases:
    """Test special cases for is_antisymmetric method."""
    
    def test_is_antisymmetric_vertex_only_as_target(self):
        """Test is_antisymmetric when vertex appears only as edge target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b appears only as target, not as key
        graph = Graph({vertex_a: [vertex_b]})
        
        # A->B exists, B->A cannot exist (B not a key), so antisymmetric
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_empty_string_vertices(self):
        """Test is_antisymmetric with vertices having empty string IDs."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        # Antisymmetric case
        graph1 = Graph({
            vertex_empty: [vertex_a],
            vertex_a: []
        })
        assert graph1.is_antisymmetric() == True
        
        # Non-antisymmetric case
        graph2 = Graph({
            vertex_empty: [vertex_a],
            vertex_a: [vertex_empty]  # Bidirectional
        })
        assert graph2.is_antisymmetric() == False
    
    def test_is_antisymmetric_multiple_edges_same_direction(self):
        """Test is_antisymmetric with multiple edges in same direction."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],  # Multiple A -> B
            vertex_b: []                               # No B -> A
        })
        
        # Multiple edges in same direction don't affect antisymmetry
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_multiple_self_loops(self):
        """Test is_antisymmetric with multiple self-loops."""
        vertex_a = Vertex("A")
        
        graph = Graph({vertex_a: [vertex_a, vertex_a, vertex_a]})
        
        # Multiple self-loops are still allowed
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_large_graph_antisymmetric(self):
        """Test is_antisymmetric with large antisymmetric graph."""
        vertices = [Vertex(str(i)) for i in range(50)]
        
        # Create directed acyclic graph (antisymmetric)
        graph_data = {}
        for i, vertex in enumerate(vertices):
            edges = [vertex]  # Self-loop
            # Add edges to higher-numbered vertices only (ensures no bidirectional edges)
            for j in range(i + 1, min(i + 4, len(vertices))):
                edges.append(vertices[j])
            graph_data[vertex] = edges
        
        graph = Graph(graph_data)
        assert graph.is_antisymmetric() == True
    
    def test_is_antisymmetric_large_graph_non_antisymmetric(self):
        """Test is_antisymmetric with large non-antisymmetric graph."""
        vertices = [Vertex(str(i)) for i in range(50)]
        
        # Create graph with many bidirectional edges
        graph_data = {}
        for i, vertex in enumerate(vertices):
            edges = [vertex]  # Self-loop
            # Add bidirectional edges with adjacent vertices
            if i > 0:
                edges.append(vertices[i - 1])
            if i < len(vertices) - 1:
                edges.append(vertices[i + 1])
            graph_data[vertex] = edges
        
        graph = Graph(graph_data)
        assert graph.is_antisymmetric() == False
    
    def test_is_antisymmetric_consistency(self):
        """Test that is_antisymmetric results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Antisymmetric graph
        graph1 = Graph({
            vertex_a: [vertex_a, vertex_b],
            vertex_b: [vertex_b]
        })
        
        # Non-antisymmetric graph
        graph2 = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_a]  # Bidirectional
        })
        
        # Multiple calls should return same result
        for _ in range(5):
            assert graph1.is_antisymmetric() == True
            assert graph2.is_antisymmetric() == False
    
    def test_is_antisymmetric_return_type(self):
        """Test that is_antisymmetric always returns a boolean."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        test_cases = [
            Graph(),                                         # Empty
            Graph({vertex_a: [vertex_a]}),                  # Self-loop only
            Graph({vertex_a: [vertex_b], vertex_b: []}),    # Antisymmetric
            Graph({vertex_a: [vertex_b], vertex_b: [vertex_a]})  # Non-antisymmetric
        ]
        
        for graph in test_cases:
            result = graph.is_antisymmetric()
            assert isinstance(result, bool)
    
    def test_is_antisymmetric_algorithm_correctness(self):
        """Test the algorithmic correctness of antisymmetry check."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # Test complex case
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_c],  # A->A (OK), A->B, A->C
            vertex_b: [vertex_b, vertex_c],            # B->B (OK), B->C
            vertex_c: [vertex_c, vertex_a]             # C->C (OK), C->A
        })
        
        # Manual check:
        # A->B: is B!=A? Yes. Is there B->A? No (B->A not in B's adjacency). OK.
        # A->C: is C!=A? Yes. Is there C->A? Yes (C->A in C's adjacency). VIOLATION.
        # Therefore: False
        
        assert graph.is_antisymmetric() == False
        
        # Fix by removing C->A
        graph._graph[vertex_c].remove(vertex_a)
        assert graph.is_antisymmetric() == True