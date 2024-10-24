from mpi4py import MPI
from typing import Dict, List, Set
from collections import deque

class Graph:
    """A class representing an undirected graph using an adjacency list.
    lua
        0 -- 1
        0 -- 2
        1 -- 3
        1 -- 4
        2 -- 5
        2 -- 6

    markdown

        0
       / \
      1   2
     / \ / \
    3  4   5 6

    Explanation of the Structure
        Node 0 is connected to nodes 1 and 2.
        Node 1 is connected to nodes 0, 3, and 4.
        Node 2 is connected to nodes 0, 5, and 6.
        Node 3 is connected to node 1.
        Node 4 is connected to node 1.
        Node 5 is connected to node 2.
        Node 6 is connected to node 2.

        This structure demonstrates how nodes are interconnected,
        allowing traversal through BFS and DFS algorithms.
        Each node can reach others according to the edges defined,
        which is why the algorithms are able to explore the
        graph starting from different nodes.

    Example output:
        [Process 0] Graph constructed with edges: {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
        [Process 0] Received adjacency list: {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
        [Process 1] Received adjacency list: {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
        [Process 1] Graph reconstructed: {0: [1, 2, 1, 2], 1: [0, 0, 3, 4, 3, 4], 2: [0, 0, 5, 6, 5, 6], 3: [1, 1], 4: [1, 1], 5: [2, 2], 6: [2, 2]}
        [Process 1] Starting BFS from node 1.
        [Process 0] Graph reconstructed: {0: [1, 2, 1, 2], 1: [0, 0, 3, 4, 3, 4], 2: [0, 0, 5, 6, 5, 6], 3: [1, 1], 4: [1, 1], 5: [2, 2], 6: [2, 2]}
        [Process 0] Starting BFS from node 0.
        [Process 0] Visiting node 0.
        [Process 0] Queuing neighbor 1.
        [Process 0] Queuing neighbor 2.
        [Process 0] Visiting node 1.
        [Process 0] Queuing neighbor 3.
        [Process 0] Queuing neighbor 4.
        [Process 0] Visiting node 2.
        [Process 0] Queuing neighbor 5.
        [Process 0] Queuing neighbor 6.
        [Process 0] Visiting node 3.
        [Process 0] Visiting node 4.
        [Process 0] Visiting node 5.
        [Process 0] Visiting node 6.
        [Process 1] Visiting node 1.
        [Process 0] BFS Result starting from node 0: [0, 1, 2, 3, 4, 5, 6]
        [Process 0] Starting DFS from node 0.
        [Process 0] Visiting node 0 in DFS.
        [Process 0] Visiting node 1 in DFS.
        [Process 0] Visiting node 3 in DFS.
        [Process 0] Visiting node 4 in DFS.
        [Process 0] Visiting node 2 in DFS.
        [Process 0] Visiting node 5 in DFS.
        [Process 0] Visiting node 6 in DFS.
        [Process 0] DFS Result starting from node 0: [0, 1, 3, 4, 2, 5, 6]
        [Process 1] Queuing neighbor 0.
        [Process 1] Queuing neighbor 3.
        [Process 1] Queuing neighbor 4.
        [Process 1] Visiting node 0.
        [Process 3] Received adjacency list: {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
        [Process 1] Queuing neighbor 2.
        [Process 3] Graph reconstructed: {0: [1, 2, 1, 2], 1: [0, 0, 3, 4, 3, 4], 2: [0, 0, 5, 6, 5, 6], 3: [1, 1], 4: [1, 1], 5: [2, 2], 6: [2, 2]}
        [Process 3] Starting BFS from node 3.
        [Process 3] Visiting node 3.
        [Process 3] Queuing neighbor 1.
        [Process 3] Visiting node 1.
        [Process 3] Queuing neighbor 0.
        [Process 3] Queuing neighbor 4.
        [Process 3] Visiting node 0.
        [Process 3] Queuing neighbor 2.
        [Process 3] Visiting node 4.
        [Process 3] Visiting node 2.
        [Process 3] Queuing neighbor 5.
        [Process 3] Queuing neighbor 6.
        [Process 3] Visiting node 5.
        [Process 3] Visiting node 6.
        [Process 3] BFS Result starting from node 3: [3, 1, 0, 4, 2, 5, 6]
        [Process 3] Starting DFS from node 3.
        [Process 3] Visiting node 3 in DFS.
        [Process 3] Visiting node 1 in DFS.
        [Process 3] Visiting node 0 in DFS.
        [Process 3] Visiting node 2 in DFS.
        [Process 3] Visiting node 5 in DFS.
        [Process 3] Visiting node 6 in DFS.
        [Process 3] Visiting node 4 in DFS.
        [Process 3] DFS Result starting from node 3: [3, 1, 0, 2, 5, 6, 4]
        [Process 1] Visiting node 3.
        [Process 1] Visiting node 4.
        [Process 1] Visiting node 2.
        [Process 1] Queuing neighbor 5.
        [Process 1] Queuing neighbor 6.
        [Process 1] Visiting node 5.
        [Process 1] Visiting node 6.
        [Process 1] BFS Result starting from node 1: [1, 0, 3, 4, 2, 5, 6]
        [Process 1] Starting DFS from node 1.
        [Process 1] Visiting node 1 in DFS.
        [Process 1] Visiting node 0 in DFS.
        [Process 1] Visiting node 2 in DFS.
        [Process 1] Visiting node 5 in DFS.
        [Process 1] Visiting node 6 in DFS.
        [Process 1] Visiting node 3 in DFS.
        [Process 1] Visiting node 4 in DFS.
        [Process 1] DFS Result starting from node 1: [1, 0, 2, 5, 6, 3, 4]
        [Process 2] Received adjacency list: {0: [1, 2], 1: [0, 3, 4], 2: [0, 5, 6], 3: [1], 4: [1], 5: [2], 6: [2]}
        [Process 2] Graph reconstructed: {0: [1, 2, 1, 2], 1: [0, 0, 3, 4, 3, 4], 2: [0, 0, 5, 6, 5, 6], 3: [1, 1], 4: [1, 1], 5: [2, 2], 6: [2, 2]}
        [Process 2] Starting BFS from node 2.
        [Process 2] Visiting node 2.
        [Process 2] Queuing neighbor 0.
        [Process 2] Queuing neighbor 5.
        [Process 2] Queuing neighbor 6.
        [Process 2] Visiting node 0.
        [Process 2] Queuing neighbor 1.
        [Process 2] Visiting node 5.
        [Process 2] Visiting node 6.
        [Process 2] Visiting node 1.
        [Process 2] Queuing neighbor 3.
        [Process 2] Queuing neighbor 4.
        [Process 2] Visiting node 3.
        [Process 2] Visiting node 4.
        [Process 2] BFS Result starting from node 2: [2, 0, 5, 6, 1, 3, 4]
        [Process 2] Starting DFS from node 2.
        [Process 2] Visiting node 2 in DFS.
        [Process 2] Visiting node 0 in DFS.
        [Process 2] Visiting node 1 in DFS.
        [Process 2] Visiting node 3 in DFS.
        [Process 2] Visiting node 4 in DFS.
        [Process 2] Visiting node 5 in DFS.
        [Process 2] Visiting node 6 in DFS.
        [Process 2] DFS Result starting from node 2: [2, 0, 1, 3, 4, 5, 6]
        BFS Results from all processes: [[0, 1, 2, 3, 4, 5, 6], [1, 0, 3, 4, 2, 5, 6], [2, 0, 5, 6, 1, 3, 4], [3, 1, 0, 4, 2, 5, 6]]
        DFS Results from all processes: [[0, 1, 3, 4, 2, 5, 6], [1, 0, 2, 5, 6, 3, 4], [2, 0, 1, 3, 4, 5, 6], [3, 1, 0, 2, 5, 6, 4]]
    """
    def __init__(self):
        # Initialize an empty adjacency list to store the graph
        self.adjacency_list: Dict[int, List[int]] = {}

    def add_edge(self, u: int, v: int) -> None:
        """Add an edge between nodes u and v in the graph.

        Args:
            u (int): The first node.
            v (int): The second node.
        """
        # Add the edge u-v to the adjacency list
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        
        # Add v to the list of neighbors of u and vice versa (undirected graph)
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)

    def get_edges(self) -> Dict[int, List[int]]:
        """Return the adjacency list of the graph.

        Returns:
            Dict[int, List[int]]: The adjacency list representation of the graph.
        """
        return self.adjacency_list


class SearchAlgorithms:
    """A class for implementing search algorithms on a graph."""
    
    def __init__(self, graph: Graph):
        # Store the adjacency list of the graph for search operations
        self.graph = graph.get_edges()

    def bfs(self, start: int) -> List[int]:
        """Perform Breadth-First Search (BFS) starting from the given node.

        Args:
            start (int): The starting node for BFS.

        Returns:
            List[int]: The order of nodes visited during BFS.
        """
        visited: Set[int] = set()  # Set to track visited nodes
        queue: deque[int] = deque([start])  # Initialize queue with the start node
        visited.add(start)  # Mark the start node as visited
        order: List[int] = []  # List to keep track of the order of traversal

        print(f"[Process {MPI.COMM_WORLD.Get_rank()}] Starting BFS from node {start}.")

        while queue:
            node = queue.popleft()  # Dequeue the front node
            order.append(node)  # Add it to the order list
            print(f"[Process {MPI.COMM_WORLD.Get_rank()}] Visiting node {node}.")
            # Explore all neighbors of the current node
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:  # If neighbor hasn't been visited
                    visited.add(neighbor)  # Mark it as visited
                    queue.append(neighbor)  # Enqueue the neighbor
                    print(f"[Process {MPI.COMM_WORLD.Get_rank()}] Queuing neighbor {neighbor}.")

        return order

    def dfs(self, start: int) -> List[int]:
        """Perform Depth-First Search (DFS) starting from the given node.

        Args:
            start (int): The starting node for DFS.

        Returns:
            List[int]: The order of nodes visited during DFS.
        """
        visited: Set[int] = set()  # Set to track visited nodes
        order: List[int] = []  # List to keep track of the order of traversal

        print(f"[Process {MPI.COMM_WORLD.Get_rank()}] Starting DFS from node {start}.")

        def dfs_recursive(node: int) -> None:
            """Helper function for recursive DFS.

            Args:
                node (int): The current node being visited.
            """
            visited.add(node)  # Mark the current node as visited
            order.append(node)  # Add it to the order list
            print(f"[Process {MPI.COMM_WORLD.Get_rank()}] Visiting node {node} in DFS.")
            # Explore all neighbors of the current node
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:  # If neighbor hasn't been visited
                    dfs_recursive(neighbor)  # Recursively visit the neighbor

        dfs_recursive(start)  # Start the DFS traversal
        return order


def main():
    """Main function to run the BFS and DFS using MPI."""
    comm = MPI.COMM_WORLD  # Get the MPI communicator
    rank = comm.Get_rank()  # Get the rank of the current process
    size = comm.Get_size()  # Get the total number of processes

    # Create a simple graph example on the root process (rank 0)
    if rank == 0:
        graph = Graph()  # Initialize a new graph
        # Add edges to the graph
        
        n = 256 # Number of nodes, modify this value to test with different number of nodes

        for i in range(n - 1):
          graph.add_edge(i, i + 1) 
        # graph.add_edge(0, 1)
        # graph.add_edge(0, 2)
        # graph.add_edge(1, 3)
        # graph.add_edge(1, 4)
        # graph.add_edge(2, 5)
        # graph.add_edge(2, 6)
        # Prepare the adjacency list for broadcasting
        adjacency_list = graph.get_edges()
        print(f"[Process {rank}] Graph constructed with edges: {adjacency_list}")
    else:
        adjacency_list = None  # Other processes will not have the graph yet

    # Broadcast the adjacency list to all processes
    adjacency_list = comm.bcast(adjacency_list, root=0)
    print(f"[Process {rank}] Received adjacency list: {adjacency_list}")

    # Create the graph object on all processes using the received adjacency list
    graph = Graph()
    for u, neighbors in adjacency_list.items():
        for v in neighbors:
            graph.add_edge(u, v)  # Rebuild the graph from the received data
    print(f"[Process {rank}] Graph reconstructed: {graph.get_edges()}")

    # Each process can perform BFS or DFS on a different starting node
    start_node = rank  # Use the process rank as the starting node

    # Instantiate the search algorithms with the constructed graph
    search_algo = SearchAlgorithms(graph)

    # Perform BFS and DFS on the starting node
    bfs_result = search_algo.bfs(start_node)
    print(f"[Process {rank}] BFS Result starting from node {start_node}: {bfs_result}")

    dfs_result = search_algo.dfs(start_node)
    print(f"[Process {rank}] DFS Result starting from node {start_node}: {dfs_result}")

    # Gather results from all processes to the root process (rank 0)
    all_bfs_results = comm.gather(bfs_result, root=0)
    all_dfs_results = comm.gather(dfs_result, root=0)

    # Only the root process will print the results
    if rank == 0:
        print("BFS Results from all processes:", all_bfs_results)
        print("DFS Results from all processes:", all_dfs_results)


if __name__ == "__main__":
    main()  # Run the main function