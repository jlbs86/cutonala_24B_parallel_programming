#DFS
class ArbolNodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def recorrido_preorden(nodo):
    if nodo is None:
        return
    print(nodo.valor, end=' ')
    recorrido_preorden(nodo.izquierda)
    recorrido_preorden(nodo.derecha)

def recorrido_nonorden(nodo):
    if nodo is None:
        return
    recorrido_nonorden(nodo.izquierda)
    print(nodo.valor, end=' ')
    recorrido_nonorden(nodo.derecha)

def recorrido_postorden(nodo):
    if nodo is None:
        return
    recorrido_postorden(nodo.izquierda)
    recorrido_postorden(nodo.derecha)
    print(nodo.valor, end=' ')

def main():
    # Crear el árbol
    raiz = ArbolNodo(1)
    raiz.izquierda = ArbolNodo(2)
    raiz.derecha = ArbolNodo(3)
    raiz.izquierda.izquierda = ArbolNodo(4)
    raiz.izquierda.derecha = ArbolNodo(5)

    print("El recorrido en Preorden es:")
    recorrido_preorden(raiz)
    print("\nEl recorrido en Desorden es:")
    recorrido_nonorden(raiz)
    print("\nEl recorrido en Postorden es:")
    recorrido_postorden(raiz)

if __name__ == "__main__":
    main()


#BFS
class ArbolNodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def altura(nodo):
    if nodo is None:
        return 0
    else:
        altura_izquierda = altura(nodo.izquierda)
        altura_derecha = altura(nodo.derecha)
        return max(altura_izquierda, altura_derecha) + 1

def a_nivel(raiz, nivel):
    if raiz is None:
        return
    if nivel == 1:
        print(raiz.valor, end=' ')
    elif nivel > 1:
        a_nivel(raiz.izquierda, nivel - 1)
        a_nivel(raiz.derecha, nivel - 1)

def orden_niveles(raiz):
    h = altura(raiz)
    for i in range(1, h + 1):
        a_nivel(raiz, i)
        print()  

def main():
    raiz = ArbolNodo(2)
    raiz.izquierda = ArbolNodo(5)
    raiz.derecha = ArbolNodo(8)
    raiz.izquierda.izquierda = ArbolNodo(11)
    raiz.izquierda.derecha = ArbolNodo(13)

    print("El orden BFS es:")
    orden_niveles(raiz)

if __name__ == "__main__":
    main()

