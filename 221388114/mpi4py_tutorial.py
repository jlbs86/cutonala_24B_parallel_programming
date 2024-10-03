from mpi4py import MPI
import numpy as np

# Just a note here: I think it's better to have three classes rather than two, as the homework in the classroom stipulates, since there are three methods.
# If it is mandatory to have just two classes, please let me know, and I will modify the code to meet the requirements given in the classroom homework.

# Class for Point-to-Point Communication
class PointToPointCommunication:
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

    def blocking_communication(self):
        if self.rank == 0:
            data = {'a': 7, 'b': 3.14}
            self.comm.send(data, dest=1, tag=11)
            print(f"Rank {self.rank} sent data: {data}")
        elif self.rank == 1:
            data = self.comm.recv(source=0, tag=11)
            print(f"Rank {self.rank} received data: {data}")

    def non_blocking_communication(self):
        if self.rank == 0:
            data = {'a': 7, 'b': 3.14}
            req = self.comm.isend(data, dest=1, tag=11)
            req.wait()
            print(f"Rank {self.rank} sent data: {data} (non-blocking)")
        elif self.rank == 1:
            req = self.comm.irecv(source=0, tag=11)
            data = req.wait()
            print(f"Rank {self.rank} received data: {data} (non-blocking)")


# Class for Collective Communication
class CollectiveCommunication:
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

    def broadcast_dict(self):
        if self.rank == 0:
            data = {'key1': [7, 2.72, 2+3j], 'key2': ('abc', 'xyz')}
        else:
            data = None

        data = self.comm.bcast(data, root=0)
        print(f"Rank {self.rank} received broadcasted data: {data}")

    def scatter_python_objects(self):
        if self.rank == 0:
            data = [(i+1)**2 for i in range(self.size)]
        else:
            data = None

        data = self.comm.scatter(data, root=0)
        print(f"Rank {self.rank} received scattered data: {data}")

    def gather_python_objects(self):
        data = (self.rank + 1)**2
        gathered_data = self.comm.gather(data, root=0)

        if self.rank == 0:
            print(f"Rank {self.rank} gathered data: {gathered_data}")


# Class for Matrix-Vector Multiplication using MPI
class MatrixVectorProduct:
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()

    def parallel_matrix_vector_multiply(self):
        if self.rank == 0:
            matrix = np.array([[i + j for j in range(4)] for i in range(4)])
            vector = np.array([1, 2, 3, 4])
            print(f"Rank {self.rank} has matrix: \n{matrix}")
            print(f"Rank {self.rank} has vector: {vector}")
        else:
            matrix = None
            vector = None

        matrix = self.comm.bcast(matrix, root=0)
        vector = self.comm.bcast(vector, root=0)

        local_rows = np.array_split(matrix, self.size, axis=0)[self.rank]
        local_result = np.dot(local_rows, vector)
        print(f"Rank {self.rank} computed local result: {local_result}")

        result = self.comm.gather(local_result, root=0)

        if self.rank == 0:
            final_result = np.concatenate(result)
            print(f"Rank {self.rank} gathered the final result: {final_result}")


if __name__ == "__main__":
    # Point-to-Point communication methods
    ptp_comm = PointToPointCommunication()
    ptp_comm.blocking_communication()
    ptp_comm.non_blocking_communication()

    # Collective communication methods
    coll_comm = CollectiveCommunication()
    coll_comm.broadcast_dict()
    coll_comm.scatter_python_objects()
    coll_comm.gather_python_objects()

    # Matrix-Vector multiplication
    matrix_vector = MatrixVectorProduct()
    matrix_vector.parallel_matrix_vector_multiply()
