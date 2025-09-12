#!/usr/bin/env python3
"""
Unit tests for Graph.get_all_edges() method.

Tests retrieval of all outgoing edges from a vertex with various configurations.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestGetAllEdges:
    """Test Graph.get_all_edges() method."""
    
    def test_get_all_edges_empty_graph(self):
        """Test get_all_edges on empty graph."""
        graph = Graph()
        vertex_a = Vertex("A")
        
        # Should raise KeyError for non-existent vertex
        with pytest.raises(KeyError):
            graph.get_all_edges(vertex_a)
    
    def test_get_all_edges_single_vertex_no_edges(self):
        """Test get_all_edges with single vertex having no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        result = graph.get_all_edges(vertex_a)
        assert result == []
        assert isinstance(result, list)
    
    def test_get_all_edges_single_vertex_self_loop(self):
        """Test get_all_edges with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        result = graph.get_all_edges(vertex_a)
        assert len(result) == 1
        assert result[0] == vertex_a
    
    def test_get_all_edges_single_outgoing_edge(self):
        """Test get_all_edges with vertex having single outgoing edge."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: []
        })
        
        result = graph.get_all_edges(vertex_a)
        assert len(result) == 1
        assert result[0] == vertex_b
        
        result_b = graph.get_all_edges(vertex_b)
        assert result_b == []
    
    def test_get_all_edges_multiple_outgoing_edges(self):
        """Test get_all_edges with vertex having multiple outgoing edges."""
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
        
        result = graph.get_all_edges(vertex_a)
        assert len(result) == 3
        assert vertex_b in result
        assert vertex_c in result
        assert vertex_d in result
        
        # Check order is preserved
        assert result == [vertex_b, vertex_c, vertex_d]
    
    def test_get_all_edges_chain_graph(self):
        """Test get_all_edges with chain graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        assert graph.get_all_edges(vertex_a) == [vertex_b]
        assert graph.get_all_edges(vertex_b) == [vertex_c]
        assert graph.get_all_edges(vertex_c) == []
    
    def test_get_all_edges_cycle_graph(self):
        """Test get_all_edges with cycle graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: [vertex_a]
        })
        
        assert graph.get_all_edges(vertex_a) == [vertex_b]
        assert graph.get_all_edges(vertex_b) == [vertex_c]
        assert graph.get_all_edges(vertex_c) == [vertex_a]
    
    def test_get_all_edges_complete_graph(self):
        """Test get_all_edges with complete graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        })
        
        result_a = graph.get_all_edges(vertex_a)
        result_b = graph.get_all_edges(vertex_b)
        result_c = graph.get_all_edges(vertex_c)
        
        assert len(result_a) == 2
        assert vertex_b in result_a and vertex_c in result_a
        
        assert len(result_b) == 2
        assert vertex_a in result_b and vertex_c in result_b
        
        assert len(result_c) == 2
        assert vertex_a in result_c and vertex_b in result_c
    
    def test_get_all_edges_with_duplicates(self):
        """Test get_all_edges when adjacency list contains duplicates."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],
            vertex_b: []
        })
        
        result = graph.get_all_edges(vertex_a)
        assert len(result) == 3
        assert all(edge == vertex_b for edge in result)
    
    def test_get_all_edges_mixed_self_and_other(self):
        """Test get_all_edges with mix of self-loops and other edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_a],
            vertex_b: [vertex_b]
        })
        
        result_a = graph.get_all_edges(vertex_a)
        assert len(result_a) == 3
        assert result_a.count(vertex_a) == 2
        assert result_a.count(vertex_b) == 1
        assert result_a == [vertex_a, vertex_b, vertex_a]
        
        result_b = graph.get_all_edges(vertex_b)
        assert result_b == [vertex_b]
    
    def test_get_all_edges_disconnected_components(self):
        """Test get_all_edges with disconnected graph components."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [],
            vertex_c: [vertex_d],
            vertex_d: []
        })
        
        assert graph.get_all_edges(vertex_a) == [vertex_b]
        assert graph.get_all_edges(vertex_b) == []
        assert graph.get_all_edges(vertex_c) == [vertex_d]
        assert graph.get_all_edges(vertex_d) == []


class TestGetAllEdgesErrorCases:
    """Test error cases for get_all_edges method."""
    
    def test_get_all_edges_vertex_not_exists(self):
        """Test get_all_edges when vertex doesn't exist in graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.get_all_edges(vertex_b)
    
    def test_get_all_edges_vertex_only_as_target(self):
        """Test get_all_edges when vertex exists only as edge target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b appears only as target, not as key
        graph = Graph({vertex_a: [vertex_b]})
        
        # Should raise KeyError because vertex_b is not a key in the graph
        with pytest.raises(KeyError):
            graph.get_all_edges(vertex_b)
    
    def test_get_all_edges_with_none(self):
        """Test get_all_edges behavior when passed None."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.get_all_edges(None)
    
    def test_get_all_edges_with_non_vertex_object(self):
        """Test get_all_edges behavior with non-Vertex object."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        with pytest.raises(KeyError):
            graph.get_all_edges("A")


class TestGetAllEdgesSpecialCases:
    """Test special cases for get_all_edges method."""
    
    def test_get_all_edges_same_id_different_object(self):
        """Test get_all_edges with vertex having same ID but different object."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a1: [vertex_b],
            vertex_b: []
        })
        
        # Should work because vertices are equal based on ID
        result1 = graph.get_all_edges(vertex_a1)
        result2 = graph.get_all_edges(vertex_a2)
        
        assert result1 == [vertex_b]
        assert result2 == [vertex_b]
        assert result1 == result2
    
    def test_get_all_edges_empty_string_vertices(self):
        """Test get_all_edges with vertices having empty string IDs."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty: [vertex_a],
            vertex_a: [vertex_empty]
        })
        
        result_empty = graph.get_all_edges(vertex_empty)
        result_a = graph.get_all_edges(vertex_a)
        
        assert result_empty == [vertex_a]
        assert result_a == [vertex_empty]
    
    def test_get_all_edges_special_character_vertices(self):
        """Test get_all_edges with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_unicode, vertex_whitespace],
            vertex_unicode: [vertex_whitespace],
            vertex_whitespace: []
        })
        
        result_special = graph.get_all_edges(vertex_special)
        result_unicode = graph.get_all_edges(vertex_unicode)
        result_whitespace = graph.get_all_edges(vertex_whitespace)
        
        assert len(result_special) == 2
        assert vertex_unicode in result_special
        assert vertex_whitespace in result_special
        
        assert result_unicode == [vertex_whitespace]
        assert result_whitespace == []
    
    def test_get_all_edges_return_type_consistency(self):
        """Test that get_all_edges always returns a list."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Test with empty adjacency list
        graph1 = Graph({vertex_a: []})
        result1 = graph1.get_all_edges(vertex_a)
        assert isinstance(result1, list)
        assert len(result1) == 0
        
        # Test with non-empty adjacency list
        graph2 = Graph({vertex_a: [vertex_b], vertex_b: []})
        result2 = graph2.get_all_edges(vertex_a)
        assert isinstance(result2, list)
        assert len(result2) == 1
    
    def test_get_all_edges_large_graph(self):
        """Test get_all_edges performance with large graph."""
        vertices = [Vertex(str(i)) for i in range(1000)]
        
        # Create a star graph: vertex 0 connects to all others
        graph_data = {vertices[0]: vertices[1:]}
        for i in range(1, 1000):
            graph_data[vertices[i]] = []
        
        graph = Graph(graph_data)
        
        # Test center vertex
        result_center = graph.get_all_edges(vertices[0])
        assert len(result_center) == 999
        assert all(v in result_center for v in vertices[1:])
        
        # Test leaf vertices
        for i in range(1, 10):  # Test first 10 leaf vertices
            result_leaf = graph.get_all_edges(vertices[i])
            assert result_leaf == []
    
    def test_get_all_edges_reference_vs_copy(self):
        """Test whether get_all_edges returns reference or copy of adjacency list."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        original_list = [vertex_b, vertex_c]
        graph = Graph({vertex_a: original_list})
        
        result = graph.get_all_edges(vertex_a)
        
        # Check if it's the same object (reference) or a copy
        # The current implementation returns the same list object
        assert result is original_list
        
        # Verify modification affects original
        result.append(vertex_a)
        assert vertex_a in graph._graph[vertex_a]
    
    def test_get_all_edges_consistency(self):
        """Test that get_all_edges results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [],
            vertex_c: []
        })
        
        # Multiple calls should return same result
        for _ in range(5):
            result = graph.get_all_edges(vertex_a)
            assert result == [vertex_b, vertex_c]
            assert len(result) == 2