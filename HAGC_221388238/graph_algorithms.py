class Algorithms:
    def __init__(self, graph):
        self.graph = graph 
    
    def bfs(self, start_node):
        print("*** BFS ***")
        # Check if the start node is in the graph
        if start_node not in self.graph:
            print("Node not found in graph")
            return -1
        # Create a list to store the visited nodes
        visited_nodes = []
        # Create a queue to store the nodes to be visited
        queue = [start_node]
        
        while queue:
            node = queue.pop(0)
            # Check if the node has been visited
            if node not in visited_nodes:
                visited_nodes.append(node)
                # Add the neighbors to the queue
                for neighbor in self.graph[node]:
                    if neighbor not in visited_nodes:
                        queue.append(neighbor)
        return visited_nodes

    def dfs(self, start_node):
        print("*** DFS ***")
        # Check if the start node is in the graph
        stack = [start_node]
        # Create a list to store the visited nodes
        visited_node = set()
        # Create a stack to store the nodes to be visited
        path = []

        while stack:
            current = stack.pop()
            # Check if the node has been visited
            if current not in visited_node:
                visited_node.add(current)
                path.append(current)
                # Add the neighbors to the stack
                for neighbor in self.graph[current]:
                    if neighbor not in visited_node:
                        stack.append(neighbor)

        return path


if __name__ == '__main__':
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'E'],
        'D': ['B', 'F'],
        'E': ['B', 'C', 'F'],
        'F': ['D', 'E']
    }

    my_instance = Algorithms(graph) 
    
    result_bfs = my_instance.bfs('D');
    print("BFS algorithm path: ", result_bfs)
    print()
    result_dfs = my_instance.dfs('D');
    print("DFS algorithm path: ", result_dfs)
