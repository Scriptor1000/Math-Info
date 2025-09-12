# Graph Theory Unit Tests

This directory contains comprehensive unit tests for the Graph theory implementation in `25-08-29/graphen.py`.

## Test Structure

The tests are organized following the request to create individual test files for each method of the Graph class, with comprehensive coverage including edge cases and special scenarios.

### Test Files

#### Vertex Tests
- `vertex/test_vertex.py` - Complete tests for the Vertex class including initialization, equality, hashing, and string representation

#### Graph Method Tests
- `graph/test_init.py` - Graph constructor tests
- `graph/test_exist_vertex.py` - Vertex existence checking tests
- `graph/test_exist_edge.py` - Edge existence checking tests  
- `graph/test_get_all_edges.py` - Edge retrieval tests
- `graph/test_get_degree.py` - Vertex degree calculation tests
- `graph/test_is_reflexive.py` - Reflexivity property tests
- `graph/test_is_symmetric.py` - Symmetry property tests
- `graph/test_is_antisymmetric.py` - Antisymmetry property tests
- `graph/test_is_transitive.py` - Transitivity property tests
- `graph/test_has_euler_circle.py` - Eulerian circle detection tests
- `graph/test_find_euler_circle.py` - Eulerian circle finding tests
- `graph/test_find_hamilton_circle.py` - Hamiltonian circle finding tests
- `graph/test_str.py` - String representation tests

#### Shared Test Resources
- `conftest.py` - Shared pytest fixtures with common graph configurations for reuse across tests

## Test Categories

Each test file includes multiple test categories:

1. **Basic Functionality Tests** - Normal operation with typical inputs
2. **Edge Cases** - Empty graphs, single vertices, special configurations
3. **Error Cases** - Invalid inputs, missing vertices, etc.
4. **Special Cases** - Empty string IDs, special characters, Unicode, large graphs
5. **Algorithm Correctness** - Verification of algorithmic implementation
6. **Consistency Tests** - Ensuring methods return consistent results

## Graph Fixtures Available

The `conftest.py` provides reusable graph fixtures:
- `empty_graph` - Empty graph
- `single_vertex_graph` - Single vertex, no edges
- `single_vertex_self_loop` - Single vertex with self-loop
- `simple_chain_graph` - A -> B -> C chain
- `simple_cycle_graph` - A -> B -> C -> A cycle
- `reflexive_graph` - All vertices have self-loops
- `symmetric_graph` - All edges are bidirectional
- `antisymmetric_graph` - No bidirectional edges (except self-loops)
- `transitive_graph` - All transitive relationships satisfied
- `complete_graph_3` - Complete graph with 3 vertices
- `euler_graph` - Graph with Eulerian circle
- `hamilton_graph` - Graph with Hamiltonian circle
- `disconnected_graph` - Multiple disconnected components
- `large_graph` - Complex graph for performance testing

## Running Tests

To run all tests:
```bash
pytest tests/
```

To run tests for a specific method:
```bash
pytest tests/graph/test_is_reflexive.py
```

To run tests with verbose output:
```bash
pytest tests/ -v
```

To run a specific test:
```bash
pytest tests/graph/test_init.py::TestGraphInit::test_init_empty_default -v
```

## Test Coverage

The tests provide comprehensive coverage including:

- **Normal cases** for each method
- **Empty graphs** and **single vertex graphs**
- **Multiple vertices** with various connectivity patterns
- **Self-loops** and **multiple edges**
- **Disconnected components**
- **Large graphs** for performance validation
- **Special vertex IDs** (empty strings, special characters, Unicode)
- **Error conditions** and **invalid inputs**
- **Algorithm correctness** verification
- **Consistency** across multiple calls
- **Return type** validation

## Test Philosophy

These tests follow the principle of testing each method in isolation while using shared fixtures to avoid duplication. Each test file focuses on one specific method, making it easy to identify and fix issues with particular functionality.

The tests are designed to be:
- **Comprehensive** - Cover all possible scenarios
- **Isolated** - Each test is independent
- **Maintainable** - Clear structure and documentation
- **Reusable** - Shared fixtures prevent code duplication
- **Educational** - Tests serve as documentation of expected behavior