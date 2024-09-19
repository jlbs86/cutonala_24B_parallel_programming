from collections import deque

def bfs(grafo, origen, objetivo):
    # Crear una cola y un conjunto para los nodos visitados
    q = deque()
    visitados = set()
    
    # Marcar el nodo de origen como visitado y agregarlo a la cola
    visitados.add(origen)
    q.append(origen)
    
    while q:
        nodo_actual = q.popleft()
        
        # Verificar si el nodo actual es el objetivo
        if nodo_actual == objetivo:
            return True
        
        # Iterar sobre todos los vecinos del nodo actual
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                # Marcar el vecino como visitado y agregarlo a la cola
                visitados.add(vecino)
                q.append(vecino)
    
    # Si se sale del bucle, el objetivo no fue encontrado
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

encontrado = bfs(grafo, origen, objetivo)

if encontrado:
    print(f"El objetivo '{objetivo}' fue encontrado a partir del nodo '{origen}'.")
else:
    print(f"El objetivo '{objetivo}' no fue encontrado a partir del nodo '{origen}'.")
