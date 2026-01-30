def greedyColoring(inputGraph):
    """
    Funktion die die Nummer der Farbe von jedem Knoten ausgibt mithilfe vom Greedy Coloring Algorithmus
    Beispiel Ausgabeformat: "A: 0, B: 1, C: 2, ..."
    """
    result = {}

    for node in inputGraph:
        # Finde die Farben der benachbarten Knoten
        neighbor_colors = set()
        for neighbor in inputGraph[node]:
            if neighbor in result:
                neighbor_colors.add(result[neighbor])
        
        # Weisen Sie die kleinste verfügbare Farbe zu
        color = 0
        while color in neighbor_colors:
            color += 1
        
        result[node] = color
    
    return result

if __name__ == "__main__":
    graph = {
        "A": ["B", "C", "D", "H"],
        "B": ["A", "C", "E", "H"],
        "C": ["A", "B", "F", "H"],
        "D": ["A", "E", "F", "H"],
        "E": ["B", "D", "F", "G"],
        "F": ["C", "D", "E", "G"],
        "G": ["E", "F", "H"],
        "H": ["A", "B", "C", "D", "G"]
    }
    
    print(f"Fertiger Gefärbter Graph: {greedyColoring(graph)}")