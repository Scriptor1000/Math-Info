#!/usr/bin/env python3
"""
Unit tests for Graph.is_transitive() method.

Tests transitivity checking: a graph is transitive if for every path u->v->w, 
there exists a direct edge u->w.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex, Graph


class TestIsTransitive:
    """Test Graph.is_transitive() method."""
    
    def test_is_transitive_empty_graph(self):
        """Test is_transitive on empty graph."""
        graph = Graph()
        
        # Empty graph is vacuously transitive
        assert graph.is_transitive() == True
    
    def test_is_transitive_single_vertex_no_edges(self):
        """Test is_transitive with single vertex having no edges."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: []})
        
        # No edges means transitive
        assert graph.is_transitive() == True
    
    def test_is_transitive_single_vertex_self_loop(self):
        """Test is_transitive with single vertex having self-loop."""
        vertex_a = Vertex("A")
        graph = Graph({vertex_a: [vertex_a]})
        
        # A->A->A requires A->A, which exists, so transitive
        assert graph.is_transitive() == True
    
    def test_is_transitive_two_vertices_simple_edge(self):
        """Test is_transitive with simple edge between two vertices."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: []
        })
        
        # No path A->?->? exists since B has no outgoing edges
        assert graph.is_transitive() == True
    
    def test_is_transitive_chain_transitive(self):
        """Test is_transitive with transitive chain A->B->C and A->C."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A->B, A->C (transitive edge)
            vertex_b: [vertex_c],            # B->C
            vertex_c: []
        })
        
        # Path A->B->C exists, A->C also exists, so transitive
        assert graph.is_transitive() == True
    
    def test_is_transitive_chain_non_transitive(self):
        """Test is_transitive with non-transitive chain A->B->C but missing A->C."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b],     # A->B
            vertex_b: [vertex_c],     # B->C
            vertex_c: []              # Missing A->C
        })
        
        # Path A->B->C exists but A->C doesn't, so not transitive
        assert graph.is_transitive() == False
    
    def test_is_transitive_triangle_complete(self):
        """Test is_transitive with complete triangle."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A->B, A->C
            vertex_b: [vertex_a, vertex_c],  # B->A, B->C
            vertex_c: [vertex_a, vertex_b]   # C->A, C->B
        })
        
        # All possible transitive relationships exist
        assert graph.is_transitive() == True
    
    def test_is_transitive_cycle_with_shortcuts(self):
        """Test is_transitive with cycle that has all transitive edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A->B, A->C (A->B->C shortcut)
            vertex_b: [vertex_c, vertex_a],  # B->C, B->A (B->C->A shortcut)
            vertex_c: [vertex_a, vertex_b]   # C->A, C->B (C->A->B shortcut)
        })
        
        # All transitive relationships satisfied
        assert graph.is_transitive() == True
    
    def test_is_transitive_longer_chain_complete(self):
        """Test is_transitive with longer chain that has all transitive edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c, vertex_d],  # A->B, A->C, A->D
            vertex_b: [vertex_c, vertex_d],            # B->C, B->D
            vertex_c: [vertex_d],                      # C->D
            vertex_d: []
        })
        
        # All transitive requirements:
        # A->B->C: need A->C ✓
        # A->B->D: need A->D ✓
        # B->C->D: need B->D ✓
        # A->C->D: need A->D ✓
        assert graph.is_transitive() == True
    
    def test_is_transitive_longer_chain_incomplete(self):
        """Test is_transitive with longer chain missing some transitive edges."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c],  # A->B, A->C (missing A->D)
            vertex_b: [vertex_c, vertex_d],  # B->C, B->D
            vertex_c: [vertex_d],            # C->D
            vertex_d: []
        })
        
        # Missing transitive edges:
        # A->B->D: need A->D (missing)
        assert graph.is_transitive() == False
    
    def test_is_transitive_with_self_loops(self):
        """Test is_transitive with self-loops in transitive graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        
        graph = Graph({
            vertex_a: [vertex_a, vertex_b],  # A->A, A->B
            vertex_b: [vertex_b]             # B->B
        })
        
        # Paths to check:
        # A->A->A: need A->A ✓
        # A->A->B: need A->B ✓
        # A->B->B: need A->B ✓
        # B->B->B: need B->B ✓
        assert graph.is_transitive() == True
    
    def test_is_transitive_disconnected_components(self):
        """Test is_transitive with disconnected components."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],  # Component 1: A->B
            vertex_b: [],          # Component 1: B isolated
            vertex_c: [vertex_d],  # Component 2: C->D
            vertex_d: []           # Component 2: D isolated
        })
        
        # No multi-step paths within components, so transitive
        assert graph.is_transitive() == True


class TestIsTransitiveSpecialCases:
    """Test special cases for is_transitive method."""
    
    def test_is_transitive_multiple_edges_same_pair(self):
        """Test is_transitive with multiple edges between same vertex pairs."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_b, vertex_c],  # A->B (twice), A->C
            vertex_b: [vertex_c, vertex_c],            # B->C (twice)
            vertex_c: []
        })
        
        # A->B->C requires A->C, which exists
        assert graph.is_transitive() == True
    
    def test_is_transitive_complex_case_transitive(self):
        """Test is_transitive with complex transitive graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        vertex_e = Vertex("E")
        
        graph = Graph({
            vertex_a: [vertex_b, vertex_c, vertex_d, vertex_e],  # A connects to all
            vertex_b: [vertex_c, vertex_d, vertex_e],            # B connects to C,D,E
            vertex_c: [vertex_d, vertex_e],                      # C connects to D,E
            vertex_d: [vertex_e],                                # D connects to E
            vertex_e: []                                         # E is sink
        })
        
        # All transitive relationships should be satisfied
        assert graph.is_transitive() == True
    
    def test_is_transitive_complex_case_non_transitive(self):
        """Test is_transitive with complex non-transitive graph."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        graph = Graph({
            vertex_a: [vertex_b],              # A->B
            vertex_b: [vertex_c, vertex_d],    # B->C, B->D
            vertex_c: [vertex_d],              # C->D
            vertex_d: []                       # Missing: A->C, A->D
        })
        
        # Missing transitive edges: A->B->C needs A->C, A->B->D needs A->D
        assert graph.is_transitive() == False
    
    def test_is_transitive_vertex_only_as_target(self):
        """Test is_transitive when vertex appears only as edge target."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # vertex_c appears only as target
        graph = Graph({
            vertex_a: [vertex_b],
            vertex_b: [vertex_c]
        })
        
        # Path A->B->C exists, but A->C cannot be checked since C is not a key
        # Current implementation should handle this correctly
        assert graph.is_transitive() == False
    
    def test_is_transitive_large_graph_transitive(self):
        """Test is_transitive with large transitive graph."""
        vertices = [Vertex(str(i)) for i in range(20)]
        
        # Create transitive closure: each vertex connects to all vertices with higher indices
        graph_data = {}
        for i, vertex in enumerate(vertices):
            edges = [vertices[j] for j in range(i + 1, len(vertices))]
            graph_data[vertex] = edges
        
        graph = Graph(graph_data)
        assert graph.is_transitive() == True
    
    def test_is_transitive_large_graph_non_transitive(self):
        """Test is_transitive with large non-transitive graph."""
        vertices = [Vertex(str(i)) for i in range(20)]
        
        # Create chain: each vertex connects only to next vertex
        graph_data = {}
        for i, vertex in enumerate(vertices):
            if i < len(vertices) - 1:
                graph_data[vertex] = [vertices[i + 1]]
            else:
                graph_data[vertex] = []
        
        graph = Graph(graph_data)
        # Chain is not transitive (missing shortcuts)
        assert graph.is_transitive() == False
    
    def test_is_transitive_consistency(self):
        """Test that is_transitive results are consistent across multiple calls."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        # Transitive graph
        graph1 = Graph({
            vertex_a: [vertex_b, vertex_c],
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        # Non-transitive graph
        graph2 = Graph({
            vertex_a: [vertex_b],     # Missing A->C
            vertex_b: [vertex_c],
            vertex_c: []
        })
        
        # Multiple calls should return same result
        for _ in range(5):
            assert graph1.is_transitive() == True
            assert graph2.is_transitive() == False
    
    def test_is_transitive_return_type(self):
        """Test that is_transitive always returns a boolean."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        
        test_cases = [
            Graph(),                                              # Empty
            Graph({vertex_a: []}),                               # Single vertex
            Graph({vertex_a: [vertex_b, vertex_c], vertex_b: [vertex_c], vertex_c: []}),  # Transitive
            Graph({vertex_a: [vertex_b], vertex_b: [vertex_c], vertex_c: []})  # Non-transitive
        ]
        
        for graph in test_cases:
            result = graph.is_transitive()
            assert isinstance(result, bool)
    
    def test_is_transitive_algorithm_correctness(self):
        """Test the algorithmic correctness of transitivity check."""
        vertex_a = Vertex("A")
        vertex_b = Vertex("B")
        vertex_c = Vertex("C")
        vertex_d = Vertex("D")
        
        # Test specific case
        graph = Graph({
            vertex_a: [vertex_b, vertex_d],    # A->B, A->D
            vertex_b: [vertex_c, vertex_d],    # B->C, B->D
            vertex_c: [vertex_d],              # C->D
            vertex_d: []
        })
        
        # Manual check for transitivity:
        # A->B: targets are [C,D]. Need A->C? No. VIOLATION.
        # A->B->C: need A->C (missing)
        # A->B->D: need A->D ✓
        # B->C->D: need B->D ✓
        # Result: False (missing A->C)
        
        assert graph.is_transitive() == False
        
        # Fix by adding A->C
        graph._graph[vertex_a].append(vertex_c)
        assert graph.is_transitive() == True