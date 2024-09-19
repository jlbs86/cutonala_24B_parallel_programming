class Nodo:
    def _initial_(self, data):
        self.dato = dato
        self.left = None
        self.right = None

def alt(nodo):
    if nodo is None:
        return 0
    else:
        Lalt = alt(nodo.left)
        Ralt = alt(nodo.right)
        return max(Lalt, Ralt) + 1

def OnLevel(root, N):
    if root is None:
        return
    if N == 1:
        print(root.data, end=' ')
    elif N > 1:
        OnLevel(root.left, N - 1)
        OnLevel(root.right, N - 1)

def NOrder(root):
    h = alt(root)
    for i in range(1, h + 1):
        OnLevel(root, i)
        print()  # Nueva línea para separar los niveles

def main():
    root = Nodo(2)
    root.left = Nodo(5)
    root.right = Nodo(8)
    root.left.left = Nodo(11)
    root.left.right = Nodo(13)

    print("Orden BFS es:")
    NOrder(root)

if _name_ == "_main_":
    main()
