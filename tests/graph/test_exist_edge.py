#!/usr/bin/env python3
"""
Unit tests for Graph.exist_edge() method.

Tests edge existence checking with various graph configurations and edge cases.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestExistEdge:
    """Test Graph.exist_edge() method."""
    
    def test_exist_edge_empty_graph(self):
        """Test exist_edge on empty graph."""
        graph = Graph()
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Should raise KeyError when accessing non-existent vertex
        with pytest.raises(KeyError):
            graph.exist_edge(vertex_a, vertex_b)
    
    def test_exist_edge_single_vertex_no_edges(self):
        """Test exist_edge with single vertex having no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        assert not graph.exist_edge(vertex_a, vertex_a)
    
    def test_exist_edge_single_vertex_self_loop(self):
        """Test exist_edge with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        assert graph.exist_edge(vertex_a, vertex_a)
    
    def test_exist_edge_simple_chain_exists(self):
        """Test exist_edge with simple chain where edges exist."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        assert graph.exist_edge(vertex_a, vertex_b)
        assert graph.exist_edge(vertex_b, vertex_c)
    
    def test_exist_edge_simple_chain_not_exists(self):
        """Test exist_edge with simple chain where edges don't exist."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        assert not graph.exist_edge(vertex_b, vertex_a)  # Reverse edge
        assert not graph.exist_edge(vertex_c, vertex_b)  # Reverse edge
        assert not graph.exist_edge(vertex_a, vertex_c)  # No direct edge
        assert not graph.exist_edge(vertex_c, vertex_a)  # No reverse edge
    
    def test_exist_edge_cycle_exists(self):
        """Test exist_edge with cycle graph where edges exist."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: [vertex_a]
        })
        
        assert graph.exist_edge(vertex_a, vertex_b)
        assert graph.exist_edge(vertex_b, vertex_c)
        assert graph.exist_edge(vertex_c, vertex_a)
    
    def test_exist_edge_multiple_edges_from_vertex(self):
        """Test exist_edge when vertex has multiple outgoing edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c, vertex_d],
            vertex_b: [],
            vertex_c: [],
            vertex_d: []
        })
        
        assert graph.exist_edge(vertex_a, vertex_b)
        assert graph.exist_edge(vertex_a, vertex_c)
        assert graph.exist_edge(vertex_a, vertex_d)
        assert not graph.exist_edge(vertex_b, vertex_a)  # No reverse edges
    
    def test_exist_edge_bidirectional(self):
        """Test exist_edge with bidirectional edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_a]
        })
        
        assert graph.exist_edge(vertex_a, vertex_b)
        assert graph.exist_edge(vertex_b, vertex_a)
    
    def test_exist_edge_with_duplicate_edges(self):
        """Test exist_edge when there are duplicate edges in adjacency list."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],
            vertex_b: []
        })
        
        # Should return True even though edge appears multiple times
        assert graph.exist_edge(vertex_a, vertex_b)
    
    def test_exist_edge_complete_graph(self):
        """Test exist_edge with complete graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        })
        
        # All possible edges should exist
        assert graph.exist_edge(vertex_a, vertex_b)
        assert graph.exist_edge(vertex_a, vertex_c)
        assert graph.exist_edge(vertex_b, vertex_a)
        assert graph.exist_edge(vertex_b, vertex_c)
        assert graph.exist_edge(vertex_c, vertex_a)
        assert graph.exist_edge(vertex_c, vertex_b)
    
    def test_exist_edge_disconnected_components(self):
        """Test exist_edge with disconnected graph components."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],  # Component 1: A -> B
            vertex_b: [],
            vertex_c: [vertex_d],  # Component 2: C -> D
            vertex_d: []
        })
        
        # Edges within components should exist
        assert graph.exist_edge(vertex_a, vertex_b)
        assert graph.exist_edge(vertex_c, vertex_d)
        
        # Edges between components should not exist
        assert not graph.exist_edge(vertex_a, vertex_c)
        assert not graph.exist_edge(vertex_a, vertex_d)
        assert not graph.exist_edge(vertex_b, vertex_c)
        assert not graph.exist_edge(vertex_b, vertex_d)
    
    def test_exist_edge_same_id_different_object(self):
        """Test exist_edge with vertices having same ID but different objects."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a1: [vertex_b],
            vertex_b: []
        })
        
        # Should work because vertices are equal based on ID
        assert graph.exist_edge(vertex_a1, vertex_b)
        assert graph.exist_edge(vertex_a2, vertex_b)  # Same ID, should work


class TestExistEdgeErrorCases:
    """Test error cases for exist_edge method."""
    
    def test_exist_edge_start_vertex_not_exists(self):
        """Test exist_edge when start vertex doesn't exist in graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({vertex_a: []})
        
        # Should raise KeyError when start vertex doesn't exist
        with pytest.raises(KeyError):
            graph.exist_edge(vertex_b, vertex_c)
    
    def test_exist_edge_end_vertex_not_in_graph(self):
        """Test exist_edge when end vertex doesn't exist as key in graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b exists only as edge target, not as key
        graph = Graph({vertex_a: [vertex_b]})
        
        # This should work fine - we're checking if A -> B exists
        assert graph.exist_edge(vertex_a, vertex_b)
        
        # But this should raise KeyError because B is not a key in graph
        with pytest.raises(KeyError):
            graph.exist_edge(vertex_b, vertex_a)
    
    def test_exist_edge_with_none_vertices(self):
        """Test exist_edge behavior when passed None vertices."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.exist_edge(None, vertex_a)
        
        with pytest.raises(TypeError):
            graph.exist_edge(vertex_a, None)
    
    def test_exist_edge_with_non_vertex_objects(self):
        """Test exist_edge behavior with non-Vertex objects."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # Should raise KeyError when using string instead of Vertex
        with pytest.raises(KeyError):
            graph.exist_edge("A", vertex_a)
        
        with pytest.raises(TypeError):
            graph.exist_edge(vertex_a, "A")


class TestExistEdgeSpecialCases:
    """Test special cases for exist_edge method."""
    
    def test_exist_edge_self_loops_multiple(self):
        """Test exist_edge with multiple self-loops."""
        vertex_a = Vertex("A")
        
        graph = Graph({vertex_a: [vertex_a, vertex_a, vertex_a]})
        
        # Should return True even with multiple self-loops
        assert graph.exist_edge(vertex_a, vertex_a)
    
    def test_exist_edge_empty_string_vertices(self):
        """Test exist_edge with vertices having empty string IDs."""
        vertex_empty1 = Vertex("")
        vertex_empty2 = Vertex("")  # Same ID
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty1: [vertex_a],
            vertex_a: [vertex_empty1]
        })
        
        assert graph.exist_edge(vertex_empty1, vertex_a)
        assert graph.exist_edge(vertex_empty2, vertex_a)  # Same ID
        assert graph.exist_edge(vertex_a, vertex_empty1)
        assert graph.exist_edge(vertex_a, vertex_empty2)  # Same ID
    
    def test_exist_edge_special_character_vertices(self):
        """Test exist_edge with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_unicode],
            vertex_unicode: [vertex_whitespace],
            vertex_whitespace: [vertex_special]
        })
        
        assert graph.exist_edge(vertex_special, vertex_unicode)
        assert graph.exist_edge(vertex_unicode, vertex_whitespace)
        assert graph.exist_edge(vertex_whitespace, vertex_special)
    
    def test_exist_edge_large_graph_performance(self):
        """Test exist_edge performance with large graph."""
        vertices = [Vertex(str(i)) for i in range(1000)]
        
        # Create chain graph
        graph_data = {}
        for i in range(1000):
            if i < 999:
                graph_data[vertices[i]] = [vertices[i + 1]]
            else:
                graph_data[vertices[i]] = []
        
        graph = Graph(graph_data)
        
        # Test edges at various positions
        assert graph.exist_edge(vertices[0], vertices[1])
        assert graph.exist_edge(vertices[500], vertices[501])
        assert graph.exist_edge(vertices[998], vertices[999])
        
        # Test non-existent edges
        assert not graph.exist_edge(vertices[1], vertices[0])  # Reverse
        assert not graph.exist_edge(vertices[0], vertices[2])  # Skip
    
    def test_exist_edge_consistency(self):
        """Test that exist_edge results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: []
        })
        
        # Multiple calls should return same result
        for _ in range(10):
            assert graph.exist_edge(vertex_a, vertex_b) == True
            assert graph.exist_edge(vertex_b, vertex_a) == False