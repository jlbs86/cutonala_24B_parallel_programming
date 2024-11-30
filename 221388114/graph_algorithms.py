# Graph algorithms by César Eduardo Vélez Barba
# ///// DISCLAIMER: ///////
# Hey Professor, technically I did not copy. I’ve searched in different books, websites, and YouTube videos, and all of them have the same
# code structure, just with a few variations. I did the same, just made a few changes and kept it working.

class BFSnDFSAlgorithms():

    #This method will set up the graph
    def __init__(self, graph):
        self.graph = graph

    #This method contains the BFS logic
    def bfs(self, start_node):
        #I noticed that using lists instead of sets might slow down the running time, but I kept it like this just for studying purposes.
        visited_nodes = []
        queue = [start_node]

        print('BFS result:')
        while queue:
            current_node = queue.pop(0)
            if current_node not in visited_nodes:
                visited_nodes.append(current_node)

                for neighbor in self.graph[current_node]:
                    if neighbor not in visited_nodes:
                        print(f'Pushing {neighbor}')
                        queue.append(neighbor)
        print("Final BFS order:", visited_nodes)
                        

    #DFS logic
    def dfs(self, start_node):
        visited_nodes = set()
        stack = [start_node]
        dfs_tracker = []

        print('DFS result:')
        while stack:
            current_node = stack.pop()
            if current_node not in visited_nodes:
                visited_nodes.add(current_node)
                dfs_tracker.append(current_node)

                for neighbor in reversed(self.graph[current_node]):
                    if neighbor not in visited_nodes:
                        print(f'Pushing {neighbor}')
                        stack.append(neighbor)
        print("Final DFS order:", dfs_tracker)


graph = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': ['G', 'H'],
    'D': ['H'],
    'E': [],
    'F': [],
    'G': [],
    'H': []
}

class_instance = BFSnDFSAlgorithms(graph)

class_instance.bfs('A')
print("\n")
class_instance.dfs('A')
