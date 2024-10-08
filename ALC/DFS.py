#en este no fue necesario importar

def DFS(grafo, inicio): #define la clase dfs e inicia por el nodo 0
    visitado = set() #para saber que nodos ya fueron visitados
    pila = [inicio] #pila de nodos desde el 0

    while pila: #mientras haya nodos en la pila va a seguir
        nodo = pila.pop() #saca el ultimo nodo
        if nodo not in visitado:
            visitado.add(nodo)
            print(nodo)
            for vecino in rev(grafo[nodo]): #recorre los vecinos en reversa
                if vecino not in visitado:
                    pila.append(vecino) #si el vecino no ha sido visitado se agrega a la pila

grafo = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4],
    3: [1],
    4: [1, 2]
}

DFS(grafo, 0)                                       