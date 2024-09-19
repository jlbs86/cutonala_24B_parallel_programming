class Nodo:
    def _initial_(self, data):
        self.data = data
        self.left = None
        self.right = None

def preorder_route(nodo):
    if nodo is None:
        return
    print(nodo.data, end=' ')
    preorder_route(nodo.left)
    preorder_route(nodo.right)

def inorder_route(nodo):
    if nodo is None:
        return
    inorder_route(nodo.left)
    print(nodo.data, end=' ')
    inorder_route(nodo.right)

def postorder_route(nodo):
    if nodo is None:
        return
    postorder_route(nodo.left)
    postorder_route(nodo.right)
    print(nodo.data, end=' ')

def main():
    # Crear el árbol
    root = Nodo(1)
    root.left = Nodo(2)
    root.right = Nodo(3)
    root.left.left = Nodo(4)
    root.left.right = Nodo(5)

    print("El recorrido en Preorden es:")
    preorder_route(root)
    print("\nEl recorrido en Inorden es:")
    inorder_route(root)
    print("\nEl recorrido en Postorden es:")
    postorder_route(root)

if _name_ == "_main_":
    main()
