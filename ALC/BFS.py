from collections import deque #libreria de python para colas

def BFS(grafo, inicio): #define la clase bfs e inicio es el nodo por el que se inicia (0)
    visitado = set() #para saber que nodos ya fueron visitados
    cola = deque([inicio]) #cola de los nodos que faltan

    while cola: #mientras haya nodos en la cola va a seguir ejecutandose
        nodo = cola.popleft() #popleft elimina el primer ndo de la cola y lo devuelve
        if nodo not in visitado: #si el nodo no esta marcado como visitado
            visitado.add(nodo) #lo marca como visitado
            print(nodo)
            for vecino in grafo[nodo]: #marca a los vecinos como visitados y append los añade a la cola
                if vecino not in visitado:
                    cola.append(vecino)

grafo = {             #          0
    0: [1, 2],        #         / \
    1: [0, 3, 4],     #        1   2
    2: [0],           #       / \   \
    3: [1],           #      3   4   
    4: [1]            #     
} 

BFS(grafo, 0)