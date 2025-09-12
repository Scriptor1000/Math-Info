#!/usr/bin/env python3
"""
Unit tests for Graph.is_reflexive() method.

Tests reflexivity checking: a graph is reflexive if every vertex has an edge to itself.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestIsReflexive:
    """Test Graph.is_reflexive() method."""
    
    def test_is_reflexive_empty_graph(self):
        """Test is_reflexive on empty graph."""
        graph = Graph()
        
        # Empty graph is vacuously reflexive (all vertices have self-loops)
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_single_vertex_with_self_loop(self):
        """Test is_reflexive with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_single_vertex_without_self_loop(self):
        """Test is_reflexive with single vertex without self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        assert graph.is_reflexive() == False
    
    def test_is_reflexive_multiple_vertices_all_have_self_loops(self):
        """Test is_reflexive when all vertices have self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A has self-loop and edge to B
            vertex_b: [vertex_b],            # B has self-loop only
            vertex_c: [vertex_c, vertex_a]   # C has self-loop and edge to A
        })
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_multiple_vertices_one_missing_self_loop(self):
        """Test is_reflexive when one vertex is missing self-loop."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A has self-loop
            vertex_b: [vertex_c],            # B missing self-loop
            vertex_c: [vertex_c]             # C has self-loop
        })
        
        assert graph.is_reflexive() == False
    
    def test_is_reflexive_multiple_vertices_none_have_self_loops(self):
        """Test is_reflexive when no vertices have self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B, no self-loop
            vertex_b: [vertex_c],  # B -> C, no self-loop
            vertex_c: [vertex_a]   # C -> A, no self-loop
        })
        
        assert graph.is_reflexive() == False
    
    def test_is_reflexive_single_vertex_multiple_self_loops(self):
        """Test is_reflexive with vertex having multiple self-loops."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a, vertex_a, vertex_a]})
        
        # Multiple self-loops still count as reflexive
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_mixed_self_loops_and_other_edges(self):
        """Test is_reflexive with mix of self-loops and other edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_c],  # A has self-loop + others
            vertex_b: [vertex_b, vertex_a],            # B has self-loop + others
            vertex_c: [vertex_c, vertex_b, vertex_a]   # C has self-loop + others
        })
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_complete_graph_with_self_loops(self):
        """Test is_reflexive with complete graph including self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_c],  # A connects to all including self
            vertex_b: [vertex_a, vertex_b, vertex_c],  # B connects to all including self
            vertex_c: [vertex_a, vertex_b, vertex_c]   # C connects to all including self
        })
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_complete_graph_without_self_loops(self):
        """Test is_reflexive with complete graph excluding self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A connects to others but not self
            vertex_b: [vertex_a, vertex_c],  # B connects to others but not self
            vertex_c: [vertex_a, vertex_b]   # C connects to others but not self
        })
        
        assert graph.is_reflexive() == False
    
    def test_is_reflexive_disconnected_components_all_reflexive(self):
        """Test is_reflexive with disconnected components, all reflexive."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # Component 1: A has self-loop
            vertex_b: [vertex_b],            # Component 1: B has self-loop
            vertex_c: [vertex_c, vertex_d],  # Component 2: C has self-loop
            vertex_d: [vertex_d]             # Component 2: D has self-loop
        })
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_disconnected_components_mixed(self):
        """Test is_reflexive with disconnected components, mixed reflexivity."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # Component 1: A has self-loop
            vertex_b: [vertex_b],            # Component 1: B has self-loop
            vertex_c: [vertex_d],            # Component 2: C missing self-loop
            vertex_d: [vertex_d]             # Component 2: D has self-loop
        })
        
        assert graph.is_reflexive() == False
    
    def test_is_reflexive_isolated_vertices_with_self_loops(self):
        """Test is_reflexive with isolated vertices that have self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a],  # Isolated with self-loop
            vertex_b: [vertex_b],  # Isolated with self-loop
            vertex_c: [vertex_c]   # Isolated with self-loop
        })
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_isolated_vertices_without_self_loops(self):
        """Test is_reflexive with isolated vertices without self-loops."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [],  # Isolated without self-loop
            vertex_b: [],  # Isolated without self-loop
            vertex_c: []   # Isolated without self-loop
        })
        
        assert graph.is_reflexive() == False


class TestIsReflexiveSpecialCases:
    """Test special cases for is_reflexive method."""
    
    def test_is_reflexive_empty_string_vertices(self):
        """Test is_reflexive with vertices having empty string IDs."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty: [vertex_empty, vertex_a],
            vertex_a: [vertex_a]
        })
        
        assert graph.is_reflexive() == True
        
        # Test case where empty string vertex is missing self-loop
        graph2 = Graph({
            vertex_empty: [vertex_a],  # Missing self-loop
            vertex_a: [vertex_a]
        })
        
        assert graph2.is_reflexive() == False
    
    def test_is_reflexive_special_character_vertices(self):
        """Test is_reflexive with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_special],
            vertex_unicode: [vertex_unicode],
            vertex_whitespace: [vertex_whitespace]
        })
        
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_same_id_different_objects(self):
        """Test is_reflexive with vertices having same ID but different objects."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        
        # Since vertices with same ID are considered equal, 
        # vertex_a2 should overwrite vertex_a1 in the dictionary
        graph = Graph({
            vertex_a1: [vertex_a1],  # Self-loop
            vertex_a2: [vertex_a2]   # This overwrites the previous entry
        })
        
        # Should have only one entry and it should be reflexive
        assert len(graph._graph) == 1
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_large_graph_all_reflexive(self):
        """Test is_reflexive performance with large reflexive graph."""
        vertices = [Vertex(str(i)) for i in range(100)]
        
        # Create graph where every vertex has self-loop and some other edges
        graph_data = {}
        for i, vertex in enumerate(vertices):
            edges = [vertex]  # Self-loop
            # Add edges to next few vertices (circular)
            for j in range(1, min(4, len(vertices))):
                target_idx = (i + j) % len(vertices)
                edges.append(vertices[target_idx])
            graph_data[vertex] = edges
        
        graph = Graph(graph_data)
        assert graph.is_reflexive() == True
    
    def test_is_reflexive_large_graph_one_missing(self):
        """Test is_reflexive performance with large graph missing one self-loop."""
        vertices = [Vertex(str(i)) for i in range(100)]
        
        # Create graph where all but one vertex have self-loops
        graph_data = {}
        for i, vertex in enumerate(vertices):
            if i == 50:  # Vertex at index 50 is missing self-loop
                edges = [vertices[(i + 1) % len(vertices)]]
            else:
                edges = [vertex, vertices[(i + 1) % len(vertices)]]
            graph_data[vertex] = edges
        
        graph = Graph(graph_data)
        assert graph.is_reflexive() == False
    
    def test_is_reflexive_consistency(self):
        """Test that is_reflexive results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Reflexive graph
        graph1 = Graph({
            vertex_a: [vertex_a, vertex_b],
            vertex_b: [vertex_b]
        })
        
        # Non-reflexive graph
        graph2 = Graph({
            vertex_a: [vertex_b],  # Missing self-loop
            vertex_b: [vertex_b]
        })
        
        # Multiple calls should return same result
        for _ in range(5):
            assert graph1.is_reflexive() == True
            assert graph2.is_reflexive() == False
    
    def test_is_reflexive_return_type(self):
        """Test that is_reflexive always returns a boolean."""
        vertex_a = Vertex("A")
        
        # Test various cases
        test_cases = [
            Graph(),                           # Empty graph
            Graph({vertex_a: []}),            # Non-reflexive
            Graph({vertex_a: [vertex_a]})     # Reflexive
        ]
        
        for graph in test_cases:
            result = graph.is_reflexive()
            assert isinstance(result, bool)
    
    def test_is_reflexive_algorithm_correctness(self):
        """Test the algorithmic correctness of reflexivity check."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # Test case: A has self-loop, B has self-loop, C does not
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_c],  # A: has self-loop
            vertex_b: [vertex_a, vertex_b],            # B: has self-loop
            vertex_c: [vertex_a, vertex_b]             # C: no self-loop
        })
        
        # Manually check: for reflexivity, every vertex must appear in its own adjacency list
        # A: vertex_a in [vertex_a, vertex_b, vertex_c] -> True
        # B: vertex_b in [vertex_a, vertex_b] -> True
        # C: vertex_c in [vertex_a, vertex_b] -> False
        # Overall: False (because C fails)
        
        assert graph.is_reflexive() == False
        
        # Now add self-loop to C
        graph._graph[vertex_c].append(vertex_c)
        assert graph.is_reflexive() == True