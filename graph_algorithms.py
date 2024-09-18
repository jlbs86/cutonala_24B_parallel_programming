class Vertex:
    def __init__(self, i):
        self.id = i
        self.visited = False
        self.level = -1
        self.parent = None
        self.neighbors = []

    def addNeighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)


class GraphAlgorithms:
    def __init__(self):
        self.vertices = {}

    def addVertex(self, neighbor):
        if neighbor not in self.vertices:
            self.vertices[neighbor] = Vertex(neighbor)

    def addEdge(self, a, b):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].addNeighbor(b)
            self.vertices[b].addNeighbor(a)


    def bfs(self, start):
        if start in self.vertices:
            queue = [start]
            self.vertices[start].visited = True
            self.vertices[start].level = 0
            print(f"({start}, {self.vertices[start].level})")  

            while len(queue) > 0:
                current = queue.pop(0)

                for neighbor in self.vertices[current].neighbors:
                    if not self.vertices[neighbor].visited:
                        queue.append(neighbor)
                        self.vertices[neighbor].visited = True
                        self.vertices[neighbor].level = self.vertices[current].level + 1
                        print(f"({neighbor}, {self.vertices[neighbor].level})")


    def dfs(self, start):
        if start in self.vertices:
            self.vertices[start].visited = True
            for node in self.vertices[start].neighbors:
                if not self.vertices[node].visited:
                    self.vertices[node].parent = start
                    print(f"({node}, {start})")
                    self.dfs(node)

 
    def reset_visits(self):
        for v in self.vertices:
            self.vertices[v].visited = False
            self.vertices[v].level = -1
            self.vertices[v].parent = None


def main():
    g = GraphAlgorithms()


    vertices = [1, 2, 3, 4, 5, 6]
    for v in vertices:
        g.addVertex(v)


    edges = [1, 2, 1, 5, 2, 3, 2, 5, 3, 4, 4, 5, 4, 6]
    for i in range(0, len(edges) - 1, 2):
        g.addEdge(edges[i], edges[i + 1])


    print("BFS Traversal (Starting from vertex 1):")
    g.bfs(1)

 
    g.reset_visits()


    print("\nDFS Traversal (Starting from vertex 1):")
    print("(1, NULL)")
    g.dfs(1)


if __name__ == "__main__":
    main()
