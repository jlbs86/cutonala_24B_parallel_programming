from mpi4py import MPI
import numpy
import numpy as np
import pickle
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

class PointToPointCommunication:
    def PythonObjects(self):
        

        if rank == 0:
            data = {'a': 7, 'b': 3.14}
            comm.send(data, dest = 1, tag = 11)
        elif rank == 1:
            data = comm.recv(source=0, tag=11)
    def PythonObjectsWNonBlocking(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        if rank == 0:
            data = {'a': 7, 'b': 3.14}
            req = comm.isend(data, dest=1, tag=11)
            req.wait()
        elif rank == 1:
            req = comm.irecv(source=0, tag=11)
            data = req.wait()

    def NumpyArr(self):

        # passing MPI datatypes explicitly
        if rank == 0:
            data = numpy.arange(1000, dtype='i')
            comm.Send([data, MPI.INT], dest=1, tag=77)
        elif rank == 1:
            data = numpy.empty(1000, dtype='i')
            comm.Recv([data, MPI.INT], source=0, tag=77)

    # automatic MPI datatype discovery
        if rank == 0:
            data = numpy.arange(100, dtype=numpy.float64)
            comm.Send(data, dest=1, tag=13)
        elif rank == 1:
            data = numpy.empty(100, dtype=numpy.float64)
            comm.Recv(data, source=0, tag=13)

class ColectiveComm:
    def BroadcastingPythonDictionary(self):

        if rank == 0:
            data = {'key1' : [7, 2.72, 2+3j],
                    'key2' : ( 'abc', 'xyz')}
        else:
            data = None
        data = comm.bcast(data, root=0)

    def ScatteringPythonObjects(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        if rank == 0:
            data = [(i+1)**2 for i in range(size)]
        else:
            data = None
        data = comm.scatter(data, root=0)
        assert data == (rank+1)**2

    def GatheringPythonObjects(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        data = (rank+1)**2
        data = comm.gather(data, root=0)
        if rank == 0:
            for i in range(size):
                assert data[i] == (i+1)**2
        else:
            assert data is None

    def BroadcastingNumpyArray(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        if rank == 0:
            data = np.arange(100, dtype='i')
        else:
            data = np.empty(100, dtype='i')
        comm.Bcast(data, root=0)
        for i in range(100):
            assert data[i] == i

    def ScatteringNumpyArray(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        sendbuf = None
        if rank == 0:
            sendbuf = np.empty([size, 100], dtype='i')
            sendbuf.T[:,:] = range(size)
        recvbuf = np.empty(100, dtype='i')
        comm.Scatter(sendbuf, recvbuf, root=0)
        assert np.allclose(recvbuf, rank)

    def GatheringNumpyArrays(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        sendbuf = np.zeros(100, dtype='i') + rank
        recvbuf = None
        if rank == 0:
            recvbuf = np.empty([size, 100], dtype='i')
        comm.Gather(sendbuf, recvbuf, root=0)
        if rank == 0:
            for i in range(size):
                assert np.allclose(recvbuf[i,:], i)

    def ParallelMatrix_Vector(self):
        def matvec(comm, A, x):
            m = A.shape[0] # local rows
            p = comm.Get_size()
            xg = numpy.zeros(m*p, dtype='d')
            comm.Allgather([x,  MPI.DOUBLE],
                        [xg, MPI.DOUBLE])
            y = numpy.dot(A, xg)
            return y

if __name__ == "__main__":

    ptp = PointToPointCommunication()
    cc = ColectiveComm()

    ptp.PythonObjects()
    ptp.PythonObjectsWNonBlocking()
    ptp.NumpyArr()

    cc.BroadcastingPythonDictionary()
    cc.ScatteringPythonObjects()
    cc.GatheringPythonObjects()
    cc.BroadcastingNumpyArray()
    cc.ScatteringNumpyArray()
    cc.GatheringNumpyArrays()
    cc.ParallelMatrix_Vector()