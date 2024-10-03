'''
  This is the code used in Google Collab, which is stored in the sample_data folder. Please copy the file in 
  case it is deleted from that folder.
  I attach the requirements.txt file for you to get the libraries used in case you run in another environment.
'''

from mpi4py import MPI
import numpy as np

# Point-to-Point Communication class
class PointToPointCommunication:
  def __init__(self):
    self.comm = MPI.COMM_WORLD
    self.rank = self.comm.Get_rank()

  # Method for sending and receiving data using pickle
  def spickle_data_communication(self):
    if self.rank == 0:
      data = {'a': 7, 'b': 3.14}
      self.comm.send(data, dest=1, tag=11)
      print(f"Rank {self.rank} received data: {data}")
    elif self.rank == 1:
      data = self.comm.recv(source=0, tag=11)
      print(f"Rank {self.rank} received data: {data}")

  # Method for non-blocking communication
  def non_block_communication(self):
    if self.rank == 0:
      data = {'a': 7, 'b': 3.14}
      req = self.comm.isend(data, dest=1, tag=11)
      req.wait()
      print(f"Rank {self.rank} received data: {data}")
    elif self.rank == 1:
      req = self.comm.irecv(source=0, tag=11)
      data = req.wait()
      print(f"Rank {self.rank} received data: {data}")

  # Method for sending and receiving numpy arrays
  def numpy_arrays(self):
    # passing MPI datatypes explicitly
    if self.rank == 0:
      data = np.arange(1000, dtype='i')
      self.comm.Send([data, MPI.INT], dest=1, tag=77)
      print(f"Rank {self.rank} received data: {data}")
    elif self.rank == 1:
      data = np.empty(1000, dtype='i')
      self.comm.Recv([data, MPI.INT], source=0, tag=77)
      print(f"Rank {self.rank} received data: {data}")

    # automatic MPI datatype discovery
    if self.rank == 0:
      data = np.arange(100, dtype=np.float64)
      self.comm.Send(data, dest=1, tag=13)
      print(f"Rank {self.rank} received data: {data}")
    elif self.rank == 1:
      data = np.empty(100, dtype=np.float64)
      self.comm.Recv(data, source=0, tag=13)
      print(f"Rank {self.rank} received data: {data}")

# Collective Communication class
class CollectiveCommunication:
  def __init__(self):
    self.comm = MPI.COMM_WORLD
    self.size = self.comm.Get_size()
    self.rank = self.comm.Get_rank()

  # Method for broadcasting a dictionary
  def broadcast_dict(self):
    if self.rank == 0:
      data = {'key1' : [7, 2.72, 2+3j],
              'key2' : ( 'abc', 'xyz')}
    else:
        data = None
    data = self.comm.bcast(data, root=0)
    print(f"Rank {self.rank} received data: {data}")

  # Method for scattering objects
  def scatter_objects(self):
    if self.rank == 0:
      data = [(i+1)**2 for i in range(self.size)]
    else:
        data = None
    data = self.comm.scatter(data, root=0)
    assert data == (self.rank+1)**2
    print(f"Rank {self.rank} received data: {data}")

  # Method for gathering objects  
  def gather_objects(self):
    data = (self.rank+1)**2
    data = self.comm.gather(data, root=0)
    if self.rank == 0:
      for i in range(self.size):
        assert data[i] == (i+1)**2
      print(f"Rank {self.rank} gathered data: {data}")
    else:
      assert data is None
      print(f"Rank {self.rank} sent data: {(self.rank+1)**2}") 

  # Method for broadcasting numpy arrays    
  def broadcast_numpy_arrays(self):
    if self.rank == 0:
      data = np.arange(100, dtype='i')
    else:
      data = np.empty(100, dtype='i')
    self.comm.Bcast(data, root=0)
    for i in range(100):
        assert data[i] == i
    print(f"Rank {self.rank} received data: {data}")

  # Method for scattering numpy arrays
  def scatter_numpy_arrays(self):
    sendbuf = None
    if self.rank == 0:
      sendbuf = np.empty([self.size, 100], dtype='i')
      sendbuf.T[:,:] = range(self.size)
    recvbuf = np.empty(100, dtype='i')
    self.comm.Scatter(sendbuf, recvbuf, root=0)
    assert np.allclose(recvbuf, self.rank)
    print(f"Rank {self.rank} received data: {recvbuf}")

  # Method for gathering numpy arrays  
  def gather_numpy_arrays(self):
    sendbuf = np.zeros(100, dtype='i') + self.rank
    recvbuf = None
    if self.rank == 0:
      recvbuf = np.empty([self.size, 100], dtype='i')
    self.comm.Gather(sendbuf, recvbuf, root=0)
    if self.rank == 0:
      for i in range(self.size):
        assert np.allclose(recvbuf[i,:], i)
      print(f"Rank {self.rank} gathered data: {recvbuf}")
    else:
      print(f"Rank {self.rank} sent data: {sendbuf}")

  # Method for parallel matrix-vector product   
  def parallel_matrix_vector_product(self, comm, A, x, m):
    m = A.shape[0] # local rows
    p = comm.Get_size()
    xg = np.zeros(m*p, dtype='d')
    comm.Allgather([x,  MPI.DOUBLE],
                   [xg, MPI.DOUBLE])
    y = np.dot(A, xg)
    return y
     
if __name__ == '__main__': 
    ptp_comm = PointToPointCommunication()
    coll_comm = CollectiveCommunication()

    ''' 
      Call point-to-point communication methods:
        Point-to-Point Communication
        Non-blocking Communication
        Numpy Arrays Communication
    '''
    ptp_comm.spickle_data_communication() 
    # ptp_comm.non_block_communication() 
    # ptp_comm.numpy_arrays()
 
    ''' 
      Call collective communication methods:
        Collective Communication
        Scatter Objects
        Gather Objects
        Broadcast Numpy Arrays 
        Scatter Numpy Arrays
        Gather Numpy Arrays
    ''' 
    # coll_comm.broadcast_dict() 
    # coll_comm.scatter_objects() 
    # coll_comm.gather_objects()  
    # coll_comm.broadcast_numpy_arrays() 
    # coll_comm.scatter_numpy_arrays() 
    # coll_comm.gather_numpy_arrays()
 