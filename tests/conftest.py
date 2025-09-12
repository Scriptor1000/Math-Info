#!/usr/bin/env python3
"""
Shared fixtures and test data for graph tests.

This module provides common graph configurations and test vertices
that can be reused across all test files.
"""
import sys
import os
import pytest

# Add the source directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '25-08-29'))

from graphen import Vertex, Graph


@pytest.fixture
def vertices():
    """Create a set of test vertices for reuse across tests."""
    return {
        'a': Vertex("A"),
        'b': Vertex("B"), 
        'c': Vertex("C"),
        'd': Vertex("D"),
        'e': Vertex("E"),
        'f': Vertex("F"),
        'g': Vertex("G"),
        'h': Vertex("H"),
        'i': Vertex("I")
    }


@pytest.fixture
def empty_graph():
    """Empty graph with no vertices."""
    return Graph()


@pytest.fixture
def single_vertex_graph(vertices):
    """Graph with single vertex, no edges."""
    return Graph({vertices['a']: []})


@pytest.fixture
def single_vertex_self_loop(vertices):
    """Graph with single vertex that has a self-loop."""
    return Graph({vertices['a']: [vertices['a']]})


@pytest.fixture
def simple_chain_graph(vertices):
    """Simple chain graph: A -> B -> C."""
    return Graph({
        vertices['a']: [vertices['b']], 
        vertices['b']: [vertices['c']], 
        vertices['c']: []
    })


@pytest.fixture
def simple_cycle_graph(vertices):
    """Simple cycle graph: A -> B -> C -> A."""
    return Graph({
        vertices['a']: [vertices['b']], 
        vertices['b']: [vertices['c']], 
        vertices['c']: [vertices['a']]
    })


@pytest.fixture
def reflexive_graph(vertices):
    """Reflexive graph where every vertex has a self-loop."""
    return Graph({
        vertices['a']: [vertices['a'], vertices['b']], 
        vertices['b']: [vertices['b'], vertices['a']]
    })


@pytest.fixture
def symmetric_graph(vertices):
    """Symmetric graph where every edge has a reverse edge."""
    return Graph({
        vertices['a']: [vertices['b']], 
        vertices['b']: [vertices['a']]
    })


@pytest.fixture
def antisymmetric_graph(vertices):
    """Antisymmetric graph with no bidirectional edges (except self-loops)."""
    return Graph({
        vertices['a']: [vertices['a'], vertices['b']], 
        vertices['b']: [vertices['b'], vertices['c']], 
        vertices['c']: [vertices['c']]
    })


@pytest.fixture
def transitive_graph(vertices):
    """Transitive graph where if A->B and B->C then A->C."""
    return Graph({
        vertices['a']: [vertices['b'], vertices['c']], 
        vertices['b']: [vertices['c']], 
        vertices['c']: []
    })


@pytest.fixture
def complete_graph_3(vertices):
    """Complete graph with 3 vertices (every vertex connected to every other)."""
    return Graph({
        vertices['a']: [vertices['b'], vertices['c']], 
        vertices['b']: [vertices['a'], vertices['c']], 
        vertices['c']: [vertices['a'], vertices['b']]
    })


@pytest.fixture
def euler_graph(vertices):
    """Graph that has an Eulerian circle (all vertices have even degree)."""
    return Graph({
        vertices['a']: [vertices['b'], vertices['d']], 
        vertices['b']: [vertices['c'], vertices['a']], 
        vertices['c']: [vertices['d'], vertices['b']], 
        vertices['d']: [vertices['a'], vertices['c']]
    })


@pytest.fixture
def hamilton_graph(vertices):
    """Graph that has a Hamiltonian circle."""
    return Graph({
        vertices['a']: [vertices['b'], vertices['c']], 
        vertices['b']: [vertices['c'], vertices['d']], 
        vertices['c']: [vertices['d'], vertices['a']], 
        vertices['d']: [vertices['a'], vertices['b']]
    })


@pytest.fixture
def disconnected_graph(vertices):
    """Graph with disconnected components."""
    return Graph({
        vertices['a']: [vertices['b']], 
        vertices['b']: [vertices['a']], 
        vertices['c']: [vertices['d']], 
        vertices['d']: [vertices['c']]
    })


@pytest.fixture
def large_graph(vertices):
    """Larger, more complex graph for comprehensive testing."""
    return Graph({
        vertices['a']: [vertices['i'], vertices['e'], vertices['f']],
        vertices['b']: [vertices['a'], vertices['c']],
        vertices['c']: [vertices['e'], vertices['i']],
        vertices['d']: [vertices['b'], vertices['c']],
        vertices['e']: [vertices['d'], vertices['f']],
        vertices['f']: [vertices['g'], vertices['a'], vertices['d']],
        vertices['g']: [vertices['h']],
        vertices['h']: [vertices['f'], vertices['a']],
        vertices['i']: [vertices['h'], vertices['b']]
    })