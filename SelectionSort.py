from mpi4py import MPI
import numpy as np

# Función de Selection Sort
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def selection_sort_parallel(a):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        data = np.array(a, dtype='i')
        print(f"Proceso {rank} está enviando el array completo: {data}")
    else:
        data = None

    # 1. Broadcasting: el proceso raíz envía el arreglo completo a todos los procesos
    data = comm.bcast(data, root=0)

    # 2. Scattering: dividir el array para que cada proceso obtenga una parte
    n = len(data)
    sub_size = n // size
    remainder = n % size

    local_data = np.empty(sub_size + (1 if rank < remainder else 0), dtype='i')

    # 3. Point-to-Point: enviar y recibir el arreglo
    if rank == 0:
        # Enviar segmentos a otros procesos
        for i in range(1, size):
            start_index = i * sub_size + min(i, remainder)
            end_index = start_index + sub_size + (1 if i < remainder else 0)
            comm.send(data[start_index:end_index], dest=i, tag=11)
            print(f"Proceso {rank} ha enviado segmento a Proceso {i}: {data[start_index:end_index]}")
        local_data = data[0:sub_size + (1 if 0 < remainder else 0)]
    else:
        # Recibir segmento desde el proceso 0
        local_data = comm.recv(source=0, tag=11)
        print(f"Proceso {rank} ha recibido segmento: {local_data}")

    print(f"Proceso {rank} tiene su parte local: {local_data}")

    # 4. Sorting local data segment using Selection Sort
    sorted_local_data = selection_sort(local_data)
    print(f"Proceso {rank} ha ordenado su parte local: {sorted_local_data}")

    # 5. Gathering: Recoger los datos ordenados de cada proceso
    sorted_data = comm.gather(sorted_local_data, root=0)

    if rank == 0:
        print("Proceso 0 ha recibido segmentos ordenados de todos los procesos:")
        for i, segment in enumerate(sorted_data):
            print(f"Segmento de proceso {i}: {segment}")

        # Merge the sorted segments
        final_data = []
        while any(len(lst) > 0 for lst in sorted_data):
            min_val, min_idx = float('inf'), -1
            for i, lst in enumerate(sorted_data):
                if len(lst) > 0 and lst[0].item() < min_val:
                    min_val, min_idx = lst[0].item(), i
            final_data.append(min_val)
            sorted_data[min_idx] = sorted_data[min_idx][1:]

        print("Array ordenado final:", final_data)

    # 6. Barrier: sincronización de todos los procesos
    comm.Barrier()

if _name_ == "_main_":
    arr = [8, 14, -8, -9, 5, -9, -3, 0, 17, 19]
    selection_sort_parallel(arr)