#!/usr/bin/env python3
"""
Unit tests for Graph.exist_vertex() method.

Tests vertex existence checking with various graph configurations and edge cases.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestExistVertex:
    """Test Graph.exist_vertex() method."""
    
    def test_exist_vertex_empty_graph(self):
        """Test exist_vertex on empty graph."""
        graph = Graph()
        vertex_a = Vertex("A")
        
        assert not graph.exist_vertex(vertex_a)
    
    def test_exist_vertex_single_vertex_exists(self):
        """Test exist_vertex when vertex exists in single-vertex graph."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        assert graph.exist_vertex(vertex_a)
    
    def test_exist_vertex_single_vertex_not_exists(self):
        """Test exist_vertex when vertex doesn't exist in single-vertex graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        graph = Graph({vertex_a: []})
        
        assert not graph.exist_vertex(vertex_b)
    
    def test_exist_vertex_multiple_vertices_exists(self):
        """Test exist_vertex when vertex exists in multi-vertex graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        assert graph.exist_vertex(vertex_a)
        assert graph.exist_vertex(vertex_b)
        assert graph.exist_vertex(vertex_c)
    
    def test_exist_vertex_multiple_vertices_not_exists(self):
        """Test exist_vertex when vertex doesn't exist in multi-vertex graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        assert not graph.exist_vertex(vertex_d)
    
    def test_exist_vertex_with_self_loop(self):
        """Test exist_vertex with vertex that has self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        assert graph.exist_vertex(vertex_a)
    
    def test_exist_vertex_isolated_vertices(self):
        """Test exist_vertex with isolated vertices (no edges)."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [],
            vertex_b: [],
            vertex_c: []
        })
        
        assert graph.exist_vertex(vertex_a)
        assert graph.exist_vertex(vertex_b)
        assert graph.exist_vertex(vertex_c)
    
    def test_exist_vertex_in_edge_target_only(self):
        """Test exist_vertex for vertex that appears only as edge target, not as key."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b appears as target but not as key in adjacency list
        graph = Graph({vertex_a: [vertex_b]})
        
        # vertex_b should not exist as a vertex in the graph according to current implementation
        # (it only exists as an edge target)
        assert graph.exist_vertex(vertex_a)
        assert not graph.exist_vertex(vertex_b)
    
    def test_exist_vertex_same_id_different_object(self):
        """Test exist_vertex with vertex having same ID but different object."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        
        graph = Graph({vertex_a1: []})
        
        # Should return True because vertices are equal based on ID
        assert graph.exist_vertex(vertex_a1)
        assert graph.exist_vertex(vertex_a2)
    
    def test_exist_vertex_case_sensitive(self):
        """Test that exist_vertex is case-sensitive."""
        vertex_a_upper = Vertex("A")
        vertex_a_lower = Vertex("a")
        
        graph = Graph({vertex_a_upper: []})
        
        assert graph.exist_vertex(vertex_a_upper)
        assert not graph.exist_vertex(vertex_a_lower)
    
    def test_exist_vertex_empty_string_id(self):
        """Test exist_vertex with vertex having empty string ID."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({vertex_empty: [vertex_a], vertex_a: []})
        
        assert graph.exist_vertex(vertex_empty)
        assert graph.exist_vertex(vertex_a)
    
    def test_exist_vertex_special_characters(self):
        """Test exist_vertex with vertex having special characters in ID."""
        vertex_special = Vertex("A@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [],
            vertex_unicode: [],
            vertex_whitespace: []
        })
        
        assert graph.exist_vertex(vertex_special)
        assert graph.exist_vertex(vertex_unicode)
        assert graph.exist_vertex(vertex_whitespace)
    
    def test_exist_vertex_large_graph(self):
        """Test exist_vertex performance and correctness with large graph."""
        vertices = [Vertex(str(i)) for i in range(1000)]
        
        # Create graph with chain structure
        graph_data = {}
        for i in range(1000):
            if i < 999:
                graph_data[vertices[i]] = [vertices[i + 1]]
            else:
                graph_data[vertices[i]] = []
        
        graph = Graph(graph_data)
        
        # Test existence of vertices at various positions
        assert graph.exist_vertex(vertices[0])      # First
        assert graph.exist_vertex(vertices[500])    # Middle
        assert graph.exist_vertex(vertices[999])    # Last
        
        # Test non-existent vertex
        non_existent = Vertex("1000")
        assert not graph.exist_vertex(non_existent)
    
    def test_exist_vertex_complete_graph(self):
        """Test exist_vertex with complete graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        })
        
        assert graph.exist_vertex(vertex_a)
        assert graph.exist_vertex(vertex_b)
        assert graph.exist_vertex(vertex_c)
        
        vertex_d = Vertex("D")
        assert not graph.exist_vertex(vertex_d)


class TestExistVertexEdgeCases:
    """Test edge cases for exist_vertex method."""
    
    def test_exist_vertex_with_none(self):
        """Test exist_vertex behavior when passed None."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # This should raise an AttributeError when trying to compare None with Vertex
        with pytest.raises(AttributeError):
            graph.exist_vertex(None)
    
    def test_exist_vertex_with_non_vertex_object(self):
        """Test exist_vertex behavior with non-Vertex object."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # Testing with string instead of Vertex should raise AttributeError
        # when comparing vertex with string (string has no 'id' attribute)
        with pytest.raises(AttributeError):
            graph.exist_vertex("A")
    
    def test_exist_vertex_after_graph_modification(self):
        """Test exist_vertex behavior after modifying graph structure."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({vertex_a: []})
        
        assert graph.exist_vertex(vertex_a)
        assert not graph.exist_vertex(vertex_b)
        
        # Modify graph by adding new vertex
        graph._graph[vertex_b] = []
        
        assert graph.exist_vertex(vertex_a)
        assert graph.exist_vertex(vertex_b)
        
        # Remove vertex
        del graph._graph[vertex_a]
        
        assert not graph.exist_vertex(vertex_a)
        assert graph.exist_vertex(vertex_b)
    
    def test_exist_vertex_with_duplicate_vertices_in_adjacency(self):
        """Test exist_vertex when vertex appears multiple times in adjacency lists."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # vertex_b appears multiple times in adjacency list of vertex_a
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],
            vertex_b: []
        })
        
        assert graph.exist_vertex(vertex_a)
        assert graph.exist_vertex(vertex_b)
    
    def test_exist_vertex_consistency(self):
        """Test that exist_vertex results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({vertex_a: []})
        
        # Multiple calls should return same result
        for _ in range(10):
            assert graph.exist_vertex(vertex_a) == True
            assert graph.exist_vertex(vertex_b) == False