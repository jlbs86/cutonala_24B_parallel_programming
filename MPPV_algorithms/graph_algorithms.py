from collections import deque

class Graph:
    def _init_(self):
        # Representamos el grafo como un diccionario de listas
        self.graph = {}

    def add_edge(self, u, v):
        # Añadir una arista de u a v
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def bfs(self, start):
        # BFS usando un conjunto para evitar ciclos y una cola (lista)
        visited = set()  # Conjunto de nodos visitados
        queue = [start]  # Usamos una lista como cola

        while queue:
            node = queue.pop(0)  # Sacamos el primer nodo de la cola
            if node not in visited:
                print(node, end=" ")  # Imprimimos el nodo visitado
                visited.add(node)  # Marcamos el nodo como visitado

                # Añadimos los vecinos no visitados a la cola
                queue.extend([neighbor for neighbor in self.graph.get(node, []) if neighbor not in visited])

    def dfs(self, start):
        # DFS usando una pila explícita (no recursivo)
        visited = set()  # Conjunto de nodos visitados
        stack = [start]  # Usamos una lista como pila

        while stack:
            node = stack.pop()  # Sacamos el último nodo de la pila
            if node not in visited:
                print(node, end=" ")  # Imprimimos el nodo visitado
                visited.add(node)  # Marcamos el nodo como visitado

                # Añadimos los vecinos no visitados a la pila
                stack.extend([neighbor for neighbor in self.graph.get(node, []) if neighbor not in visited])


# Ejemplo de uso
g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(1, 4)
g.add_edge(2, 5)
g.add_edge(2, 6)

print("Recorrido BFS (desde el nodo 0):")
g.bfs(0)  # Resultado esperado: 0 1 2 3 4 5 6

print("\nRecorrido DFS (desde el nodo 0):")
g.dfs(0)  # Resultado esperado: 0 2 6 5 1 4 3