class GraphSearch:
    def __init__(self, graph):
        self.graph = graph

    def DFS(self, origen, objetivo):
        stack = []
        stack.append(origen)
        visited = set()
        visited.add(origen)
        
        while stack:
            nodoActual = stack.pop()
            if nodoActual == objetivo:
                return True
            for w in self.graph[nodoActual]:
                if w not in visited:
                    stack.append(w)
                    visited.add(w)
        return False

    def BFS(self, origen, objetivo):
        from collections import deque
        queue = deque([origen])
        visited = set()
        visited.add(origen)
        
        while queue:
            nodoActual = queue.popleft()
            if nodoActual == objetivo:
                return True
            for w in self.graph[nodoActual]:
                if w not in visited:
                    visited.add(w)
                    queue.append(w)
        return False

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': ['I', 'J'],
    'F': ['K'],
    'G': ['L'],
    'H': [],
    'I': [],
    'J': [],
    'K': [],
    'L': []
}
search = GraphSearch(graph)

# Busqueda desde al objetivo
resultado_dfs = search.DFS('A', 'F')
print(f"DFS encontró el objetivo: {resultado_dfs}")

# Busqueda desde al objetivo
resultado_bfs = search.BFS('A', 'F')
print(f"BFS encontró el objetivo: {resultado_bfs}")
