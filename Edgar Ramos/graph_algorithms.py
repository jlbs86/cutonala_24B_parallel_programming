class Graph:
    def __init__(self):
        # Initialize the graph as an empty dictionary
        self.graph = {}

    def add_edge(self, node, neighbor):
        # Add a neighbor to the adjacency list of the node
        if node not in self.graph:
            self.graph[node] = []
        self.graph[node].append(neighbor)
    
    def bfs(self, start):
        # Breadth-First Search (BFS) implementation
        queue = [start]
        visited = set([start])
        
        while queue:
            current_node = queue.pop(0)
            print(f"Visiting node: {current_node}")
            
            for neighbor in self.graph.get(current_node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    def dfs(self, start, visited=None):
        # Depth-First Search (DFS) implementation
        if visited is None:
            visited = set()
        
        visited.add(start)
        print(f"Visiting node: {start}")
        
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

# Example usage
g = Graph()
g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'D')
g.add_edge('B', 'E')
g.add_edge('C', 'F')

print("BFS traversal:")
g.bfs('A')

print("\nDFS traversal:")
g.dfs('A')