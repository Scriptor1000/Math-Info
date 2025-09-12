#!/usr/bin/env python3
"""
Unit tests for the Vertex class.

Tests all methods of the Vertex class including edge cases and special scenarios.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '25-08-29'))

from graphen import Vertex


class TestVertexInit:
    """Test Vertex initialization."""
    
    def test_init_normal_string(self):
        """Test vertex creation with normal string ID."""
        vertex = Vertex("A")
        assert vertex.id == "A"
    
    def test_init_empty_string(self):
        """Test vertex creation with empty string ID."""
        vertex = Vertex("")
        assert vertex.id == ""
    
    def test_init_numeric_string(self):
        """Test vertex creation with numeric string ID."""
        vertex = Vertex("123")
        assert vertex.id == "123"
    
    def test_init_special_characters(self):
        """Test vertex creation with special characters."""
        vertex = Vertex("A@#$%")
        assert vertex.id == "A@#$%"
    
    def test_init_unicode(self):
        """Test vertex creation with Unicode characters."""
        vertex = Vertex("αβγ")
        assert vertex.id == "αβγ"
    
    def test_init_long_string(self):
        """Test vertex creation with very long string."""
        long_id = "A" * 1000
        vertex = Vertex(long_id)
        assert vertex.id == long_id


class TestVertexEquality:
    """Test Vertex equality comparison."""
    
    def test_equality_same_id(self):
        """Test that vertices with same ID are equal."""
        v1 = Vertex("A")
        v2 = Vertex("A")
        assert v1 == v2
    
    def test_equality_different_id(self):
        """Test that vertices with different IDs are not equal."""
        v1 = Vertex("A")
        v2 = Vertex("B")
        assert v1 != v2
    
    def test_equality_empty_id(self):
        """Test equality with empty string IDs."""
        v1 = Vertex("")
        v2 = Vertex("")
        assert v1 == v2
    
    def test_equality_case_sensitive(self):
        """Test that equality is case-sensitive."""
        v1 = Vertex("A")
        v2 = Vertex("a")
        assert v1 != v2
    
    def test_equality_whitespace_sensitive(self):
        """Test that equality is whitespace-sensitive."""
        v1 = Vertex("A")
        v2 = Vertex(" A")
        v3 = Vertex("A ")
        assert v1 != v2
        assert v1 != v3
        assert v2 != v3
    
    def test_equality_with_none(self):
        """Test equality comparison with None."""
        vertex = Vertex("A")
        with pytest.raises(AttributeError):
            # This should raise AttributeError because None doesn't have 'id' attribute
            vertex == None


class TestVertexHash:
    """Test Vertex hash functionality."""
    
    def test_hash_same_id(self):
        """Test that vertices with same ID have same hash."""
        v1 = Vertex("A")
        v2 = Vertex("A")
        assert hash(v1) == hash(v2)
    
    def test_hash_different_id(self):
        """Test that vertices with different IDs typically have different hashes."""
        v1 = Vertex("A")
        v2 = Vertex("B")
        # Note: Hash collisions are possible but unlikely for different strings
        assert hash(v1) != hash(v2)
    
    def test_hash_consistency(self):
        """Test that hash value is consistent across multiple calls."""
        vertex = Vertex("A")
        hash1 = hash(vertex)
        hash2 = hash(vertex)
        assert hash1 == hash2
    
    def test_hash_empty_string(self):
        """Test hash of vertex with empty string ID."""
        vertex = Vertex("")
        hash_value = hash(vertex)
        assert isinstance(hash_value, int)
    
    def test_vertices_in_set(self):
        """Test that vertices can be used in sets (requires proper hash implementation)."""
        v1 = Vertex("A")
        v2 = Vertex("A")  # Same ID
        v3 = Vertex("B")  # Different ID
        
        vertex_set = {v1, v2, v3}
        # Set should contain only 2 unique vertices (A and B)
        assert len(vertex_set) == 2
        assert v1 in vertex_set
        assert v2 in vertex_set
        assert v3 in vertex_set
    
    def test_vertices_as_dict_keys(self):
        """Test that vertices can be used as dictionary keys."""
        v1 = Vertex("A")
        v2 = Vertex("A")  # Same ID
        v3 = Vertex("B")  # Different ID
        
        vertex_dict = {}
        vertex_dict[v1] = "value1"
        vertex_dict[v3] = "value2"
        
        # Accessing with v2 (same ID as v1) should work
        assert vertex_dict[v1] == "value1"
        assert vertex_dict[v2] == "value1"  # Same ID, so should access same value
        assert vertex_dict[v3] == "value2"


class TestVertexString:
    """Test Vertex string representation."""
    
    def test_str_normal(self):
        """Test string representation of normal vertex."""
        vertex = Vertex("A")
        assert str(vertex) == "A"
    
    def test_str_empty_string(self):
        """Test string representation of vertex with empty string ID."""
        vertex = Vertex("")
        assert str(vertex) == ""
    
    def test_str_numeric_string(self):
        """Test string representation of vertex with numeric string ID."""
        vertex = Vertex("123")
        assert str(vertex) == "123"
    
    def test_str_special_characters(self):
        """Test string representation with special characters."""
        vertex = Vertex("A@#$%")
        assert str(vertex) == "A@#$%"
    
    def test_str_unicode(self):
        """Test string representation with Unicode characters."""
        vertex = Vertex("αβγ")
        assert str(vertex) == "αβγ"
    
    def test_str_consistency_with_id(self):
        """Test that string representation is always consistent with ID."""
        test_ids = ["A", "", "123", "A@#$%", "αβγ", " spaces ", "\n\t"]
        for test_id in test_ids:
            vertex = Vertex(test_id)
            assert str(vertex) == test_id


class TestVertexIntegration:
    """Integration tests for Vertex functionality."""
    
    def test_vertex_in_list(self):
        """Test vertex behavior in lists."""
        v1 = Vertex("A")
        v2 = Vertex("A")  # Same ID
        v3 = Vertex("B")
        
        vertices = [v1, v2, v3]
        assert len(vertices) == 3
        assert v1 in vertices
        assert v2 in vertices
        assert v3 in vertices
    
    def test_vertex_comparison_transitivity(self):
        """Test that vertex equality is transitive."""
        v1 = Vertex("A")
        v2 = Vertex("A")
        v3 = Vertex("A")
        
        assert v1 == v2
        assert v2 == v3
        assert v1 == v3  # Transitivity
    
    def test_vertex_comparison_symmetry(self):
        """Test that vertex equality is symmetric."""
        v1 = Vertex("A")
        v2 = Vertex("A")
        
        assert v1 == v2
        assert v2 == v1  # Symmetry
    
    def test_vertex_comparison_reflexivity(self):
        """Test that vertex equality is reflexive."""
        vertex = Vertex("A")
        assert vertex == vertex  # Reflexivity