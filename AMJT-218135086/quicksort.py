from mpi4py import MPI
import numpy as np
from collections import Counter

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr)//2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)

def generate_random_data(n):
    return np.random.randint(1, 10000, size=n, dtype=np.int32)

def parallel_quicksort():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # El proceso root genera los datos
    if rank == 0:
        n = 1000  # Puedes cambiar este número para ordenar más o menos elementos
        data = generate_random_data(n)
        original_data = data.copy()
    else:
        data = None
        original_data = None
    
    # Broadcast del tamaño del array
    if rank == 0:
        n = np.array(len(data), dtype=np.int32)
    else:
        n = np.array(0, dtype=np.int32)
    
    comm.Bcast(n, root=0)
    
    # Calcular las divisiones para cada proceso
    counts = np.array([n // size + (1 if i < n % size else 0) for i in range(size)], dtype=np.int32)
    displs = np.array([sum(counts[:i]) for i in range(size)], dtype=np.int32)
    
    # Crear buffer local
    local_data = np.empty(counts[rank], dtype=np.int32)
    
    # Distribuir los datos
    if rank == 0:
        comm.Scatterv([data, counts, displs, MPI.INT32_T], local_data)
    else:
        comm.Scatterv(None, local_data)
    
    # Ordenar datos locales
    local_sorted = np.array(quicksort(local_data.tolist()), dtype=np.int32)
    
    # Sincronizar procesos
    comm.Barrier()
    
    # Recolectar resultados
    if rank == 0:
        final_data = np.empty(n, dtype=np.int32)
    else:
        final_data = None
    
    comm.Gatherv(sendbuf=local_sorted, recvbuf=[final_data, counts, displs, MPI.INT32_T], root=0)
    
    # Ordenamiento final en el proceso root
    if rank == 0:
        final_sorted = quicksort(final_data.tolist())
        return np.array(final_sorted), original_data
    return None

def verify_sorting(original, sorted_data):
    print("\n=== RESULTADOS DEL ORDENAMIENTO ===")
    print(f"Tamaño del array: {len(sorted_data)} elementos")
    print(f"\nPrimeros 5 números:")
    print(f"Original: {original[:5]}")
    print(f"Ordenado: {sorted_data[:5]}")
    print(f"\nÚltimos 5 números:")
    print(f"Original: {original[-5:]}")
    print(f"Ordenado: {sorted_data[-5:]}")
    
    is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
    print(f"\n¿Números ordenados correctamente?: {is_sorted}")

if __name__ == "__main__":
    result = parallel_quicksort()
    
    if MPI.COMM_WORLD.Get_rank() == 0:  # Solo el proceso principal muestra resultados
        sorted_data, original_data = result
        verify_sorting(original_data, sorted_data)