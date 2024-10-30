from mpi4py import MPI
import numpy as np

class MultiplicacionMatricesDistribuida:
    def __init__(self, comm):
        self.comm = comm
        self.rank = comm.Get_rank()
        self.size = comm.Get_size()

    def scatter_matrix(self, A):
        if self.rank == 0:
            A_chunks = np.array_split(A, self.size, axis=0)
            print(f"Master process {self.rank} scattering A_chunks: {A_chunks}")
        else:
            A_chunks = None
        A_chunk = self.comm.scatter(A_chunks, root=0)
        print(f"Process {self.rank} received A_chunk: {A_chunk}")
        return A_chunk

    def broadcast_matrix(self, B):
        if self.rank == 0:
            print(f"Master process {self.rank} broadcasting B: {B}")
        B = self.comm.bcast(B, root=0)
        print(f"Process {self.rank} received B: {B}")
        return B

    def gather_matrix(self, C_partial):
        C_chunks = self.comm.gather(C_partial, root=0)
        if self.rank == 0:
            C = np.vstack(C_chunks)
            print("Resulting matrix C:")
            print(C)
            return C
        return None

    def matrix_multiply(self, A, B):
        C = np.zeros((A.shape[0], B.shape[1]))
        for i in range(A.shape[0]):
            for j in range(B.shape[1]):
                for k in range(A.shape[1]):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def execute(self, A, B):
        A_chunk = self.scatter_matrix(A)
        B = self.broadcast_matrix(B)
        C_partial = self.matrix_multiply(A_chunk, B)
        print(f"Process {self.rank} calculated C_partial: {C_partial}")

        self.comm.Barrier()
        print(f"Process {self.rank} reached Barrier")

        self.gather_matrix(C_partial)

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    multiplicacion_distribuida = MultiplicacionMatricesDistribuida(comm)

    if comm.Get_rank() == 0:
        A = np.array([[1., 0.5], [0.5, 1.]])
        B = np.array([[1., 1.5], [1.5, 1.]])
    else:
        A = None
        B = None

    multiplicacion_distribuida.execute(A, B)
    comm.Barrier()
    MPI.Finalize()