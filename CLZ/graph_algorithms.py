from collections import deque

class Graph:
    def __init__(self):
        # Inicialización de un diccionario para representar el grafo
        self.graph = {}

    def add_edge(self, u, v):
        # Añade una arista de u a v en el grafo
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def BFS(self, start):
        # Recorrido en anchura (BFS)
        visited = set()  # Para evitar visitar nodos repetidos
        queue = deque([start])  # Usamos una cola para el BFS
        visited.add(start)

        while queue:
            node = queue.popleft()
            print(node, end=" ")  # Imprimir el nodo actual

            # Recorre los nodos adyacentes
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def DFS(self, start):
        # Recorrido en profundidad (DFS)
        visited = set()  # Para evitar visitar nodos repetidos
        stack = [start]  # Usamos una pila para el DFS

        while stack:
            node = stack.pop()
            if node not in visited:
                print(node, end=" ")  # Imprimir el nodo actual
                visited.add(node)

                # Añade los vecinos en la pila
                for neighbor in reversed(self.graph.get(node, [])):  # Recorremos al revés para respetar el orden
                    if neighbor not in visited:
                        stack.append(neighbor)

# Ejemplo de uso
g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 5)
g.add_edge(2, 6)

print("Recorrido BFS (desde el nodo 0):")
g.BFS(0)  # Resultado esperado: 0 1 2 3 4 5 6

print("\nRecorrido DFS (desde el nodo 0):")
g.DFS(0)  # Resultado esperado: 0 1 3 4 2 5 6