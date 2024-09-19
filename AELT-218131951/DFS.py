def DFS(Grafo, origen, objetivo):
    stack = []  # Usamos una lista para implementar la pila
    stack.append(origen)
    visited = set()  # Usamos un conjunto para marcar los nodos visitados
    visited.add(origen)

    while stack:
        nodoActual = stack.pop()
        if nodoActual == objetivo:
            return True  # Se ha encontrado el objetivo
        
        for w in Grafo[nodoActual]:
            if w not in visited:
                stack.append(w)
                visited.add(w)

    return False

# Definir el grafo
grafo = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Ejemplo de uso
origen = 'A'
objetivo = 'F'

encontrado = DFS(grafo, origen, objetivo)

if encontrado:
    print(f"El objetivo '{objetivo}' fue encontrado a partir del nodo '{origen}'.")
else:
    print(f"El objetivo '{objetivo}' no fue encontrado a partir del nodo '{origen}'.")
