import itertools
import copy

# Rückgabe von Information über die Existenz von Kanten von einem gegebenen t zu allen s
# Bsp.: get_s(graph, 0) = [0, 1, 0, 0] für den ersten Graphen
def get_s(graph, t) -> list:
    return graph[t]

# Rückgabe von Information über die Existenz von Kanten von einem gegebenen s zu allen t
# Bsp.: get_t(graph, 2) = [0, 1, 0, 1] für den ersten Graphen
def get_t(graph, s) -> list:
    return [t[s] for t in graph]

def heiratssatz_von_hall(graph) -> bool:
    # 1) Alle Kombinationen von Knoten einer "Partei" erlangen
    # 2) Für jede Kombination überprüfen: Kardinalität >= Anzahl an Knoten der Kombination
    combinations = [itertools.combinations(range(len(graph)), r) for r in range(1, len(graph) + 1)]
    for combination in itertools.chain.from_iterable(combinations):
        connectioned = set()
        for t in combination:
            for s, has_edge in enumerate(graph[t]):
                if has_edge:
                    connectioned.add(s)
        if len(connectioned) < len(combination):
            return False
    return True

# Initialisierung des Graphen als Adjazensmatrix
#         s0 s1 s2 s3
graph = [[0, 1, 0, 0], # t0
         [0, 1, 1, 0], # t1
         [1, 0, 0, 1], # t2
         [1, 0, 1, 0]] # t3

# graph = [[0, 1, 0, 0, 0, 0],
#         [0, 1, 1, 0, 0, 0],
#         [1, 0, 0, 1, 0, 0],
#         [1, 0, 1, 0, 1, 1],
#         [0, 0, 0, 0, 1, 0],
#         [0, 1, 0, 0, 0, 0]]

print("Heiratssatz von Hall:", heiratssatz_von_hall(graph))