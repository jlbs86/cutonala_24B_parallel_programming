class Grafo:
    def __init__(self):
        self.grafo = {}
    
    def agregar_arista(self, nodo, vecino):
        if nodo not in self.grafo:
            self.grafo[nodo] = []
        self.grafo[nodo].append(vecino)
    
    def bfs(self, inicio):
        visitados = []
        cola = [inicio]
        
        while cola:
            nodo = cola.pop(0)
            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.grafo.get(nodo, []):
                    if vecino not in visitados:
                        cola.append(vecino)
        
        return visitados
    
    def dfs(self, inicio):
        visitados = []
        pila = [inicio]
        
        while pila:
            nodo = pila.pop()
            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.grafo.get(nodo, []):
                    if vecino not in visitados:
                        pila.append(vecino)
        
        return visitados

g = Grafo()
g.agregar_arista(0, 1)
g.agregar_arista(0, 2)
g.agregar_arista(1, 2)
g.agregar_arista(2, 0)
g.agregar_arista(2, 3)
g.agregar_arista(3, 3)

print("BFS:", g.bfs(2))
print("DFS:", g.dfs(2))