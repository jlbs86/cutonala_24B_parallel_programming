from mpi4py import MPI
import numpy as np

class point_to_point_communication:    
    def pickle():
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        if rank == 0:
            data = {'a': 7, 'b': 3.14}
            comm.send(data, dest=1, tag=11)
            print(f"Proceso {rank} envio los datos: {data}")
        elif rank == 1:
            data = comm.recv(source=0, tag=11)
            print(f"Proceso {rank} recibio los datos: {data}")
    
    def non_blocking():
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        if rank == 0:
            data = {'a': 7, 'b': 3.14}
            req = comm.isend(data, dest=1, tag=11)  # Envío no bloqueante
            req.wait()  # Espera a que el envío se complete
            print(f"Proceso {rank} envio los datos: {data}")
        elif rank == 1:
            req = comm.irecv(source=0, tag=11)  # Recepción no bloqueante
            data = req.wait()  # Espera a que la recepción se complete
            print(f"Proceso {rank} recibio los datos: {data}")
    
    def arrays():
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        # Envío explícito con MPI datatypes
        if rank == 0:
            data = np.arange(1000, dtype='i')
            comm.Send([data, MPI.INT], dest=1, tag=77)
            print(f"Proceso {rank} envio un array de enteros con {len(data)} elementos.")
        elif rank == 1:
            data = np.empty(1000, dtype='i')
            comm.Recv([data, MPI.INT], source=0, tag=77)
            print(f"Proceso {rank} recibio un array de enteros: {data[:10]}...")  # Muestra los primeros 10 elementos

        # Envío con detección automática del tipo de datos
        if rank == 0:
            data = np.arange(100, dtype=np.float64)
            comm.Send(data, dest=1, tag=13)
            print(f"Proceso {rank} envio un array de flotantes con {len(data)} elementos.")
        elif rank == 1:
            data = np.empty(100, dtype=np.float64)
            comm.Recv(data, source=0, tag=13)
            print(f"Proceso {rank} recibio un array de flotantes: {data[:10]}...")  # Muestra los primeros 10 elementos


class collective_communication:

    def broadcasting():
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        if rank == 0:
            data = {'key1': [7, 2.72, 2 + 3j], 'key2': ('abc', 'xyz')}
        else:
            data = None
        data = comm.bcast(data, root=0)

        print(f"Proceso {rank} recibio los datos: {data}")

    def scattering():
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        if rank == 0:
            data = [(i + 1) ** 2 for i in range(size)]
        else:
            data = None
        data = comm.scatter(data, root=0)

        print(f"Proceso {rank} recibio el valor: {data}")
        assert data == (rank + 1) ** 2

    def gathering():
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        data = (rank + 1) ** 2
        gathered_data = comm.gather(data, root=0)

        if rank == 0:
            print(f"Proceso {rank} recibio los valores: {gathered_data}")
            for i in range(size):
                assert gathered_data[i] == (i + 1) ** 2
        else:
            print(f"Proceso {rank} no recibio datos.")

    def broadcasting_array():
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        if rank == 0:
            data = np.arange(100, dtype='i')
        else:
            data = np.empty(100, dtype='i')
        comm.Bcast(data, root=0)

        print(f"Proceso {rank} recibio el array: {data[:10]}...")  # Muestra solo los primeros 10 elementos
        for i in range(100):
            assert data[i] == i

    def scattering_numpy_arrays():
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        sendbuf = None
        if rank == 0:
            sendbuf = np.empty([size, 100], dtype='i')
            sendbuf.T[:, :] = range(size)
        recvbuf = np.empty(100, dtype='i')
        comm.Scatter(sendbuf, recvbuf, root=0)

        print(f"Proceso {rank} recibio el array: {recvbuf[:10]}...")  # Muestra solo los primeros 10 elementos
        assert np.allclose(recvbuf, rank)

    def gathering_numpy_arrays():
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        sendbuf = np.zeros(100, dtype='i') + rank
        recvbuf = None
        if rank == 0:
            recvbuf = np.empty([size, 100], dtype='i')
        comm.Gather(sendbuf, recvbuf, root=0)

        if rank == 0:
            print(f"Proceso {rank} recibio el array combinado: {recvbuf[:, :10]}...")  # Muestra los primeros 10 de cada proceso
            for i in range(size):
                assert np.allclose(recvbuf[i, :], i)

    # Producto paralelo matriz-vector
    def matvec(comm, A, x):
        m = A.shape[0]  # filas locales
        p = comm.Get_size()
        xg = np.zeros(m * p, dtype='d')
        comm.Allgather([x, MPI.DOUBLE], [xg, MPI.DOUBLE])
        y = np.dot(A, xg)
        return y
    
    
if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
            

    if rank == 0:
        print("Point-to-Point Communication (Pickle) Example:")
    point_to_point_communication.pickle()

    if rank == 0:
        print("\nPoint-to-Point Communication (Non-blocking) Example:")
    point_to_point_communication.non_blocking()

    if rank == 0:
        print("\nPoint-to-Point Communication (Arrays) Example:")
    point_to_point_communication.arrays()

    if rank == 0:
        print("Broadcasting Example:")
    collective_communication.broadcasting()

    if rank == 0:
        print("\nScattering Example:")
    collective_communication.scattering()

    if rank == 0:
        print("\nGathering Example:")
    collective_communication.gathering()

    if rank == 0:
        print("\nBroadcasting Array Example:")
    collective_communication.broadcasting_array()

    if rank == 0:
        print("\nScattering NumPy Arrays Example:")
    collective_communication.scattering_numpy_arrays()

    if rank == 0:
        print("\nGathering NumPy Arrays Example:")
    collective_communication.gathering_numpy_arrays()
    