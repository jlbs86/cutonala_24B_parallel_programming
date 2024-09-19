class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None

def recorrido_preorden(nodo):
    if nodo is None:
        return
    print(nodo.dato, end=' ')
    recorrido_preorden(nodo.izq)
    recorrido_preorden(nodo.der)

def recorrido_inorden(nodo):
    if nodo is None:
        return
    recorrido_inorden(nodo.izq)
    print(nodo.dato, end=' ')
    recorrido_inorden(nodo.der)

def recorrido_postorden(nodo):
    if nodo is None:
        return
    recorrido_postorden(nodo.izq)
    recorrido_postorden(nodo.der)
    print(nodo.dato, end=' ')

def main():
    # Crear el árbol
    root = Nodo(1)
    root.izq = Nodo(2)
    root.der = Nodo(3)
    root.izq.izq = Nodo(4)
    root.izq.der = Nodo(5)

    print("El recorrido en Preorden es:")
    recorrido_preorden(root)
    print("\nEl recorrido en Inorden es:")
    recorrido_inorden(root)
    print("\nEl recorrido en Postorden es:")
    recorrido_postorden(root)

if __name__ == "__main__":
    main()
