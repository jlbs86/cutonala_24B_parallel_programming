from mpi4py import MPI

# Initialize the MPI environment
comm = MPI.COMM_WORLD
size = comm.Get_size()  # Total number of processes
rank = comm.Get_rank()  # Rank of the current process

# Define a basic linked list node structure
class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

# Function to create a linked list for demonstration
def create_linked_list(values):
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Process 0 creates a linked list and converts it to a list of values
if rank == 0:
    # Create a linked list with sample values
    linked_list_values = [i for i in range(size)]  # List with 'size' number of nodes
    print(f"Process 0: Initial linked list values: {linked_list_values}")
else:
    linked_list_values = None

# Broadcast the length of the linked list to all processes
linked_list_length = comm.bcast(len(linked_list_values) if rank == 0 else None, root=0)
comm.Barrier()

# Scatter the values of the linked list nodes across all processes
scattered_value = comm.scatter(linked_list_values if rank == 0 else None, root=0)
print(f"Process {rank}: Received node value {scattered_value} after scatter.")

# Each process performs a computation on its node value
processed_value = scattered_value * 2  # Example operation on node

# Gather the processed node values back to process 0
gathered_results = comm.gather(processed_value, root=0)

# Process 0 reconstructs the processed list and prints it
if rank == 0:
    print(f"Process 0: Processed linked list values: {gathered_results}")

# Point-to-point communication for demonstration
if rank == 0:
    # Process 0 sends a message to process 1
    comm.send("Linked list node processed", dest=1)
    print("Process 0: Sent message to process 1.")
elif rank == 1:
    # Process 1 receives the message from process 0
    message = comm.recv(source=0)
    print(f"Process 1: Received message: {message}")
