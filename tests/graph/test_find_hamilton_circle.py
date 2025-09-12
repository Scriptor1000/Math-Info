#!/usr/bin/env python3
"""
Unit tests for Graph.find_hamilton_circle() method.

Tests Hamiltonian circle finding using brute force permutation checking.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestFindHamiltonCircle:
    """Test Graph.find_hamilton_circle() method."""
    
    def test_find_hamilton_circle_empty_graph(self):
        """Test find_hamilton_circle on empty graph."""
        graph = Graph()
        
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_single_vertex_no_edges(self):
        """Test find_hamilton_circle with single vertex having no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # Single vertex without self-loop cannot form Hamilton circle
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_single_vertex_self_loop(self):
        """Test find_hamilton_circle with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        # Single vertex with self-loop can form Hamilton circle
        result = graph.find_hamilton_circle()
        assert result == (vertex_a,)
    
    def test_find_hamilton_circle_two_vertices_no_hamilton(self):
        """Test find_hamilton_circle with two vertices, no Hamilton circle."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: []           # B has no outgoing edges
        })
        
        # Cannot return to A from B, so no Hamilton circle
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_two_vertices_bidirectional(self):
        """Test find_hamilton_circle with bidirectional edge between two vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],  # A -> B
            vertex_b: [vertex_a]   # B -> A
        })
        
        # Can form Hamilton circle: A -> B -> A
        result = graph.find_hamilton_circle()
        assert len(result) == 2
        assert vertex_a in result
        assert vertex_b in result
    
    def test_find_hamilton_circle_triangle_complete(self):
        """Test find_hamilton_circle with complete triangle."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        })
        
        # Complete triangle should have Hamilton circle
        result = graph.find_hamilton_circle()
        assert len(result) == 3
        assert vertex_a in result
        assert vertex_b in result
        assert vertex_c in result
    
    def test_find_hamilton_circle_triangle_incomplete(self):
        """Test find_hamilton_circle with incomplete triangle."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],     # A -> B
            vertex_b: [vertex_c],     # B -> C
            vertex_c: []              # C has no outgoing edges (missing C -> A)
        })
        
        # Cannot return to A from C, so no Hamilton circle
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_triangle_cycle(self):
        """Test find_hamilton_circle with triangle cycle."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],     # A -> B
            vertex_b: [vertex_c],     # B -> C
            vertex_c: [vertex_a]      # C -> A
        })
        
        # Forms cycle visiting all vertices
        result = graph.find_hamilton_circle()
        assert len(result) == 3
        assert vertex_a in result
        assert vertex_b in result
        assert vertex_c in result
    
    def test_find_hamilton_circle_square_complete(self):
        """Test find_hamilton_circle with complete 4-vertex graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c, vertex_d],
            vertex_b: [vertex_a, vertex_c, vertex_d],
            vertex_c: [vertex_a, vertex_b, vertex_d],
            vertex_d: [vertex_a, vertex_b, vertex_c]
        })
        
        # Complete graph should have Hamilton circle
        result = graph.find_hamilton_circle()
        assert len(result) == 4
        assert all(v in result for v in [vertex_a, vertex_b, vertex_c, vertex_d])
    
    def test_find_hamilton_circle_square_cycle(self):
        """Test find_hamilton_circle with 4-cycle."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],     # A -> B
            vertex_b: [vertex_c],     # B -> C
            vertex_c: [vertex_d],     # C -> D
            vertex_d: [vertex_a]      # D -> A
        })
        
        # 4-cycle should have Hamilton circle
        result = graph.find_hamilton_circle()
        assert len(result) == 4
        assert all(v in result for v in [vertex_a, vertex_b, vertex_c, vertex_d])
    
    def test_find_hamilton_circle_path_no_hamilton(self):
        """Test find_hamilton_circle with path (no cycle)."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],     # A -> B
            vertex_b: [vertex_c],     # B -> C
            vertex_c: [vertex_d],     # C -> D
            vertex_d: []              # D has no outgoing edges
        })
        
        # Path cannot form Hamilton circle
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_disconnected_no_hamilton(self):
        """Test find_hamilton_circle with disconnected graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],     # Component 1: A <-> B
            vertex_b: [vertex_a],
            vertex_c: [vertex_d],     # Component 2: C <-> D
            vertex_d: [vertex_c]
        })
        
        # Disconnected graph cannot have Hamilton circle visiting all vertices
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_with_extra_edges(self):
        """Test find_hamilton_circle with cycle plus extra edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A -> B, A -> C (extra edge)
            vertex_b: [vertex_c],            # B -> C
            vertex_c: [vertex_a]             # C -> A
        })
        
        # Should still find Hamilton circle despite extra edges
        result = graph.find_hamilton_circle()
        assert len(result) == 3
        assert all(v in result for v in [vertex_a, vertex_b, vertex_c])


class TestFindHamiltonCircleEdgeCases:
    """Test edge cases for find_hamilton_circle method."""
    
    def test_find_hamilton_circle_with_self_loops(self):
        """Test find_hamilton_circle with self-loops in the graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A has self-loop + edge to B
            vertex_b: [vertex_b, vertex_c],  # B has self-loop + edge to C
            vertex_c: [vertex_c, vertex_a]   # C has self-loop + edge to A
        })
        
        # Self-loops don't affect Hamilton circle (visits each vertex once)
        result = graph.find_hamilton_circle()
        assert len(result) == 3
        assert all(v in result for v in [vertex_a, vertex_b, vertex_c])
    
    def test_find_hamilton_circle_multiple_edges_same_pair(self):
        """Test find_hamilton_circle with multiple edges between same pairs."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],  # Multiple A -> B
            vertex_b: [vertex_c],                      # B -> C
            vertex_c: [vertex_a, vertex_a]             # Multiple C -> A
        })
        
        # Multiple edges don't affect Hamilton circle existence
        result = graph.find_hamilton_circle()
        assert len(result) == 3
        assert all(v in result for v in [vertex_a, vertex_b, vertex_c])
    
    def test_find_hamilton_circle_return_type(self):
        """Test that find_hamilton_circle returns correct types."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        test_cases = [
            Graph(),                                              # Empty -> []
            Graph({vertex_a: []}),                               # Single, no self-loop -> []
            Graph({vertex_a: [vertex_a]}),                       # Single, self-loop -> tuple
            Graph({vertex_a: [vertex_b], vertex_b: []}),         # No Hamilton -> []
            Graph({vertex_a: [vertex_b], vertex_b: [vertex_a]})  # Has Hamilton -> tuple
        ]
        
        for graph in test_cases:
            result = graph.find_hamilton_circle()
            assert isinstance(result, (list, tuple))
            if result == []:
                assert isinstance(result, list)
            else:
                assert isinstance(result, tuple)
    
    def test_find_hamilton_circle_consistency(self):
        """Test that find_hamilton_circle is consistent."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: [vertex_a]
        })
        
        # Multiple calls should return consistent results
        results = [graph.find_hamilton_circle() for _ in range(3)]
        
        # All results should be either all empty or all non-empty
        all_empty = all(len(r) == 0 for r in results)
        all_non_empty = all(len(r) > 0 for r in results)
        assert all_empty or all_non_empty
        
        # If non-empty, should contain same vertices (order might differ)
        if all_non_empty:
            for result in results[1:]:
                assert set(result) == set(results[0])
    
    def test_find_hamilton_circle_algorithm_correctness(self):
        """Test algorithmic correctness by verifying the returned path."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_c, vertex_a],
            vertex_c: [vertex_a, vertex_b]
        })
        
        result = graph.find_hamilton_circle()
        
        if len(result) > 0:
            # Should visit each vertex exactly once
            assert len(set(result)) == len(result), "Should visit each vertex exactly once"
            
            # Should visit all vertices in the graph
            assert set(result) == set(graph._graph.keys()), "Should visit all vertices"
            
            # Verify edges exist for the path
            for i in range(len(result)):
                current = result[i]
                next_vertex = result[(i + 1) % len(result)]  # Wrap around for circle
                assert next_vertex in graph._graph[current], f"Edge {current} -> {next_vertex} should exist"


class TestFindHamiltonCircleSpecialCases:
    """Test special cases for find_hamilton_circle method."""
    
    def test_find_hamilton_circle_empty_string_vertices(self):
        """Test find_hamilton_circle with vertices having empty string IDs."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty: [vertex_a],
            vertex_a: [vertex_empty]
        })
        
        result = graph.find_hamilton_circle()
        assert len(result) == 2
        assert vertex_empty in result
        assert vertex_a in result
    
    def test_find_hamilton_circle_special_character_vertices(self):
        """Test find_hamilton_circle with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_unicode],
            vertex_unicode: [vertex_whitespace],
            vertex_whitespace: [vertex_special]
        })
        
        result = graph.find_hamilton_circle()
        assert len(result) == 3
        assert all(v in result for v in [vertex_special, vertex_unicode, vertex_whitespace])
    
    def test_find_hamilton_circle_performance_small_complete_graph(self):
        """Test find_hamilton_circle performance with small complete graph."""
        vertices = [Vertex(str(i)) for i in range(5)]
        
        # Create complete graph
        graph_data = {}
        for vertex in vertices:
            graph_data[vertex] = [v for v in vertices if v != vertex]
        
        graph = Graph(graph_data)
        result = graph.find_hamilton_circle()
        
        # Complete graph should always have Hamilton circle
        assert len(result) == 5
        assert set(result) == set(vertices)
    
    def test_find_hamilton_circle_performance_cycle_graph(self):
        """Test find_hamilton_circle with cycle graph."""
        vertices = [Vertex(str(i)) for i in range(6)]
        
        # Create cycle
        graph_data = {}
        for i, vertex in enumerate(vertices):
            next_vertex = vertices[(i + 1) % len(vertices)]
            graph_data[vertex] = [next_vertex]
        
        graph = Graph(graph_data)
        result = graph.find_hamilton_circle()
        
        # Cycle should have Hamilton circle
        assert len(result) == 6
        assert set(result) == set(vertices)
    
    def test_find_hamilton_circle_no_hamilton_complex(self):
        """Test find_hamilton_circle with complex graph that has no Hamilton circle."""
        # Create a graph where one vertex is not reachable from the cycle
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],     # A -> B
            vertex_b: [vertex_c],     # B -> C
            vertex_c: [vertex_b],     # C -> B (dead end from cycle perspective)
            vertex_d: [vertex_a]      # D -> A (D not reachable from A-B-C component)
        })
        
        # Cannot visit all vertices in a single cycle
        result = graph.find_hamilton_circle()
        assert result == []
    
    def test_find_hamilton_circle_preserves_graph(self):
        """Test that find_hamilton_circle doesn't modify the original graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        original_graph_data = {
            vertex_a: [vertex_b],
            vertex_b: [vertex_a]
        }
        graph = Graph(original_graph_data)
        
        # Store original state
        original_a_edges = list(graph._graph[vertex_a])
        original_b_edges = list(graph._graph[vertex_b])
        
        # Find Hamilton circle
        result = graph.find_hamilton_circle()
        
        # Verify graph is unchanged
        assert graph._graph[vertex_a] == original_a_edges
        assert graph._graph[vertex_b] == original_b_edges