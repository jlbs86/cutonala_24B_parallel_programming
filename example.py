from mpi4py import MPI
import threading
import time

def thread_funtion(rank, comm):
    while True:
        status = f"Hilo {rank} activo"
        print(f"Estado de {rank}: {status}")

        dest_rank = (rank + 1) % size
        comm.send(status, dest=dest_rank)

        source_rank = (rank - 1) % size
        received_status = comm.recv(source=source_rank)
        print(f"Recibo en {rank}: {received_status}")

        time.sleep(1)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

threads = []
for i in range(size):
    thread = threading.Thread(target=thread_funtion, args=(i, comm))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()