#!/usr/bin/env python3
"""
Unit tests for Graph.__init__() method.

Tests Graph initialization with various input scenarios including edge cases.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestGraphInit:
    """Test Graph initialization."""
    
    def test_init_empty_default(self):
        """Test creating empty graph with default parameter."""
        graph = Graph()
        assert graph._graph == {}
    
    def test_init_empty_explicit(self):
        """Test creating empty graph with explicit None parameter."""
        graph = Graph(None)
        assert graph._graph == {}
    
    def test_init_empty_dict(self):
        """Test creating graph with empty dictionary."""
        graph = Graph({})
        assert graph._graph == {}
    
    def test_init_single_vertex_no_edges(self):
        """Test creating graph with single vertex and no edges."""
        vertex_a = Vertex("A")
        graph_data = {vertex_a: []}
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 1
        assert vertex_a in graph._graph
        assert graph._graph[vertex_a] == []
    
    def test_init_single_vertex_self_loop(self):
        """Test creating graph with single vertex that has self-loop."""
        vertex_a = Vertex("A")
        graph_data = {vertex_a: [vertex_a]}
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 1
        assert vertex_a in graph._graph
        assert graph._graph[vertex_a] == [vertex_a]
    
    def test_init_simple_chain(self):
        """Test creating simple chain graph A -> B -> C."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph_data = {
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 3
        assert graph._graph[vertex_a] == [vertex_b]
        assert graph._graph[vertex_b] == [vertex_c]
        assert graph._graph[vertex_c] == []
    
    def test_init_simple_cycle(self):
        """Test creating simple cycle graph A -> B -> C -> A."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph_data = {
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: [vertex_a]
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 3
        assert graph._graph[vertex_a] == [vertex_b]
        assert graph._graph[vertex_b] == [vertex_c]
        assert graph._graph[vertex_c] == [vertex_a]
    
    def test_init_multiple_edges_from_vertex(self):
        """Test creating graph with vertex having multiple outgoing edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph_data = {
            vertex_a: [vertex_b, vertex_c, vertex_d],
            vertex_b: [],
            vertex_c: [],
            vertex_d: []
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 4
        assert len(graph._graph[vertex_a]) == 3
        assert vertex_b in graph._graph[vertex_a]
        assert vertex_c in graph._graph[vertex_a]
        assert vertex_d in graph._graph[vertex_a]
    
    def test_init_complete_graph(self):
        """Test creating complete graph where every vertex connects to every other."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph_data = {
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 3
        for vertex in [vertex_a, vertex_b, vertex_c]:
            assert len(graph._graph[vertex]) == 2
    
    def test_init_with_duplicates_in_adjacency_list(self):
        """Test creating graph with duplicate edges in adjacency list."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Note: The current implementation doesn't prevent duplicates
        # This test documents the current behavior
        graph_data = {
            vertex_a: [vertex_b, vertex_b, vertex_b],
            vertex_b: []
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 2
        assert graph._graph[vertex_a] == [vertex_b, vertex_b, vertex_b]
    
    def test_init_isolated_vertices(self):
        """Test creating graph with isolated vertices (no edges)."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph_data = {
            vertex_a: [],
            vertex_b: [],
            vertex_c: []
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 3
        for vertex in [vertex_a, vertex_b, vertex_c]:
            assert graph._graph[vertex] == []
    
    def test_init_mixed_connectivity(self):
        """Test creating graph with mixed connectivity patterns."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph_data = {
            vertex_a: [vertex_b],           # A connects to B
            vertex_b: [vertex_a],           # B connects back to A
            vertex_c: [vertex_c],           # C has self-loop
            vertex_d: []                    # D is isolated
        }
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 4
        assert graph._graph[vertex_a] == [vertex_b]
        assert graph._graph[vertex_b] == [vertex_a]
        assert graph._graph[vertex_c] == [vertex_c]
        assert graph._graph[vertex_d] == []
    
    def test_init_reference_independence(self):
        """Test that graph initialization shares references to adjacency lists."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        original_data = {vertex_a: [vertex_b], vertex_b: []}
        graph = Graph(original_data)
        
        # Modify original data
        original_data[vertex_a].append(vertex_a)
        
        # Graph should be affected because it shares the same list objects
        # This documents the current behavior of the implementation
        assert len(graph._graph[vertex_a]) == 2
        assert vertex_b in graph._graph[vertex_a]
        assert vertex_a in graph._graph[vertex_a]
    
    def test_init_large_graph(self):
        """Test creating graph with many vertices."""
        vertices = [Vertex(str(i)) for i in range(100)]
        
        # Create a simple chain
        graph_data = {}
        for i in range(100):
            if i < 99:
                graph_data[vertices[i]] = [vertices[i + 1]]
            else:
                graph_data[vertices[i]] = []
        
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 100
        for i in range(99):
            assert graph._graph[vertices[i]] == [vertices[i + 1]]
        assert graph._graph[vertices[99]] == []
    
    def test_init_vertices_with_same_id_different_objects(self):
        """Test behavior when vertices have same ID but are different objects."""
        vertex_a1 = Vertex("A")
        vertex_a2 = Vertex("A")  # Same ID, different object
        vertex_b = Vertex("B")
        
        # Due to how Python dict keys work with __eq__ and __hash__, 
        # vertices with same ID should be treated as the same key
        graph_data = {
            vertex_a1: [vertex_b],
            vertex_a2: [vertex_b],  # This should overwrite the previous entry
            vertex_b: []
        }
        graph = Graph(graph_data)
        
        # Should have only 2 entries because vertex_a1 and vertex_a2 are equal
        assert len(graph._graph) == 2
        assert vertex_a1 in graph._graph
        assert vertex_a2 in graph._graph  # Should be True due to equality
        assert vertex_b in graph._graph


class TestGraphInitEdgeCases:
    """Test edge cases for Graph initialization."""
    
    def test_init_with_non_vertex_keys(self):
        """Test that non-Vertex keys in graph data work (though not recommended)."""
        # This documents current behavior - the implementation doesn't strictly enforce Vertex types
        graph_data = {"A": ["B"], "B": []}
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 2
        assert "A" in graph._graph
        assert "B" in graph._graph
    
    def test_init_with_non_list_values(self):
        """Test behavior with non-list adjacency values."""
        vertex_a = Vertex("A")
        
        # This should work with any iterable
        graph_data = {vertex_a: tuple([vertex_a])}  # Using tuple instead of list
        graph = Graph(graph_data)
        
        assert len(graph._graph) == 1
        assert graph._graph[vertex_a] == tuple([vertex_a])
    
    def test_init_preserves_original_structure(self):
        """Test that initialization preserves the exact structure passed in."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        # Use a specific list object
        edge_list = [vertex_b]
        graph_data = {vertex_a: edge_list, vertex_b: []}
        graph = Graph(graph_data)
        
        # The graph should contain the same list object (not a copy)
        assert graph._graph[vertex_a] is edge_list