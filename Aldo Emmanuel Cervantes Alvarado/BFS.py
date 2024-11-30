class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izq = None
        self.der = None

def alt(nodo):
    if nodo is None:
        return 0
    else:
        Lalt = alt(nodo.izq)
        Ralt = alt(nodo.der)
        return max(Lalt, Ralt) + 1

def ANivel(root, N):
    if root is None:
        return
    if N == 1:
        print(root.dato, end=' ')
    elif N > 1:
        ANivel(root.izq, N - 1)
        ANivel(root.der, N - 1)

def OrdenN(root):
    h = alt(root)
    for i in range(1, h + 1):
        ANivel(root, i)
        print()  # Nueva línea para separar los niveles

def main():
    root = Nodo(2)
    root.izq = Nodo(5)
    root.der = Nodo(8)
    root.izq.izq = Nodo(11)
    root.izq.der = Nodo(13)

    print("Orden BFS es:")
    OrdenN(root)

if __name__ == "__main__":
    main()
