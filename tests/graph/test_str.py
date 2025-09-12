#!/usr/bin/env python3
"""
Unit tests for Graph.__str__() method.

Tests string representation of graphs showing adjacency list format.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestGraphStr:
    """Test Graph.__str__() method."""
    
    def test_str_empty_graph(self):
        """Test string representation of empty graph."""
        graph = Graph()
        
        result = str(graph)
        assert result == ""
    
    def test_str_single_vertex_no_edges(self):
        """Test string representation of single vertex with no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        result = str(graph)
        assert "A: []" in result
    
    def test_str_single_vertex_self_loop(self):
        """Test string representation of single vertex with self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        result = str(graph)
        assert "A: ['A']" in result
    
    def test_str_two_vertices_simple_edge(self):
        """Test string representation of two vertices with simple edge."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: []
        })
        
        result = str(graph)
        lines = result.split('\n')
        
        # Should contain both vertices
        vertex_lines = [line for line in lines if line.strip()]
        assert len(vertex_lines) == 2
        
        # Check content (order might vary)
        assert any("A: ['B']" in line for line in vertex_lines)
        assert any("B: []" in line for line in vertex_lines)
    
    def test_str_two_vertices_bidirectional(self):
        """Test string representation of two vertices with bidirectional edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_a]
        })
        
        result = str(graph)
        lines = result.split('\n')
        vertex_lines = [line for line in lines if line.strip()]
        
        assert len(vertex_lines) == 2
        assert any("A: ['B']" in line for line in vertex_lines)
        assert any("B: ['A']" in line for line in vertex_lines)
    
    def test_str_triangle_graph(self):
        """Test string representation of triangle graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_a, vertex_c],
            vertex_c: [vertex_a, vertex_b]
        })
        
        result = str(graph)
        lines = result.split('\n')
        vertex_lines = [line for line in lines if line.strip()]
        
        assert len(vertex_lines) == 3
        
        # Check that all vertices and their connections are represented
        result_text = '\n'.join(vertex_lines)
        assert "A:" in result_text
        assert "B:" in result_text
        assert "C:" in result_text
    
    def test_str_multiple_edges_same_target(self):
        """Test string representation with multiple edges to same target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_b],
            vertex_b: []
        })
        
        result = str(graph)
        
        # Should show all multiple edges
        assert "A: ['B', 'B', 'B']" in result
        assert "B: []" in result
    
    def test_str_complex_graph(self):
        """Test string representation of more complex graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_d],
            vertex_c: [vertex_d],
            vertex_d: []
        })
        
        result = str(graph)
        lines = result.split('\n')
        vertex_lines = [line for line in lines if line.strip()]
        
        assert len(vertex_lines) == 4
        
        # Verify each vertex appears with correct adjacency format
        result_text = '\n'.join(vertex_lines)
        for vertex_name in ['A', 'B', 'C', 'D']:
            assert f"{vertex_name}:" in result_text
    
    def test_str_with_self_loops_and_other_edges(self):
        """Test string representation with mix of self-loops and other edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b, vertex_a],
            vertex_b: [vertex_b]
        })
        
        result = str(graph)
        
        # Should show all edges including multiple self-loops
        assert "A: ['A', 'B', 'A']" in result
        assert "B: ['B']" in result
    
    def test_str_isolated_vertices(self):
        """Test string representation with isolated vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [],
            vertex_b: [],
            vertex_c: []
        })
        
        result = str(graph)
        lines = result.split('\n')
        vertex_lines = [line for line in lines if line.strip()]
        
        assert len(vertex_lines) == 3
        
        # All should show empty adjacency lists
        for line in vertex_lines:
            assert ": []" in line


class TestGraphStrSpecialCases:
    """Test special cases for Graph.__str__() method."""
    
    def test_str_empty_string_vertex(self):
        """Test string representation with vertex having empty string ID."""
        vertex_empty = Vertex("")
        vertex_a = Vertex("A")
        
        graph = Graph({
            vertex_empty: [vertex_a],
            vertex_a: []
        })
        
        result = str(graph)
        
        # Should handle empty string vertex ID
        assert ": ['A']" in result  # Empty string vertex
        assert "A: []" in result
    
    def test_str_special_character_vertices(self):
        """Test string representation with vertices having special characters."""
        vertex_special = Vertex("@#$%")
        vertex_unicode = Vertex("αβγ")
        vertex_whitespace = Vertex(" A B ")
        
        graph = Graph({
            vertex_special: [vertex_unicode],
            vertex_unicode: [vertex_whitespace],
            vertex_whitespace: []
        })
        
        result = str(graph)
        
        # Should handle special characters properly
        assert "@#$%" in result
        assert "αβγ" in result
        assert " A B " in result
    
    def test_str_numeric_string_vertices(self):
        """Test string representation with numeric string vertices."""
        vertex_1 = Vertex("1")
        vertex_2 = Vertex("2")
        vertex_123 = Vertex("123")
        
        graph = Graph({
            vertex_1: [vertex_2, vertex_123],
            vertex_2: [vertex_123],
            vertex_123: []
        })
        
        result = str(graph)
        
        assert "1:" in result
        assert "2:" in result
        assert "123:" in result
    
    def test_str_return_type(self):
        """Test that __str__ always returns a string."""
        vertex_a = Vertex("A")
        
        test_cases = [
            Graph(),                              # Empty
            Graph({vertex_a: []}),               # Single vertex
            Graph({vertex_a: [vertex_a]})        # With edges
        ]
        
        for graph in test_cases:
            result = str(graph)
            assert isinstance(result, str)
    
    def test_str_no_trailing_newline_single_vertex(self):
        """Test that string representation doesn't have trailing newline for single vertex."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        result = str(graph)
        assert not result.endswith('\n')
    
    def test_str_no_trailing_newline_multiple_vertices(self):
        """Test that string representation doesn't have trailing newline for multiple vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: []
        })
        
        result = str(graph)
        assert not result.endswith('\n')
    
    def test_str_format_consistency(self):
        """Test that string format is consistent."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        result = str(graph)
        lines = result.split('\n')
        
        # Each line should follow "vertex: [list]" format
        for line in lines:
            if line.strip():  # Skip empty lines
                assert ': [' in line
                assert line.endswith(']')
    
    def test_str_large_graph(self):
        """Test string representation with larger graph."""
        vertices = [Vertex(str(i)) for i in range(10)]
        
        # Create chain graph
        graph_data = {}
        for i, vertex in enumerate(vertices):
            if i < len(vertices) - 1:
                graph_data[vertex] = [vertices[i + 1]]
            else:
                graph_data[vertex] = []
        
        graph = Graph(graph_data)
        result = str(graph)
        
        lines = result.split('\n')
        vertex_lines = [line for line in lines if line.strip()]
        
        # Should have 10 lines, one for each vertex
        assert len(vertex_lines) == 10
        
        # Each vertex should appear
        for i in range(10):
            assert f"{i}:" in result
    
    def test_str_consistency(self):
        """Test that string representation is consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_a]
        })
        
        # Multiple calls should return same result
        results = [str(graph) for _ in range(3)]
        
        # All results should be identical
        for result in results[1:]:
            assert result == results[0]
    
    def test_str_vertex_order_deterministic(self):
        """Test that vertex order in string representation is deterministic."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # Create same graph multiple times
        graphs = [Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c],
            vertex_c: [vertex_a]
        }) for _ in range(3)]
        
        # String representations should be identical
        str_results = [str(graph) for graph in graphs]
        for result in str_results[1:]:
            assert result == str_results[0]
    
    def test_str_edge_list_format(self):
        """Test that edge lists are properly formatted as Python lists."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [],
            vertex_c: [vertex_a]
        })
        
        result = str(graph)
        
        # Should use single quotes for vertex strings in lists
        # and proper list formatting
        assert "['B', 'C']" in result or "['C', 'B']" in result
        assert "[]" in result
        assert "['A']" in result