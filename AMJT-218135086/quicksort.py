from mpi4py import MPI
import numpy as np
import random
import time
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

def sequential_quicksort(data):
    start_time = time.time()
    sorted_data = quicksort(data.tolist())
    end_time = time.time()
    return np.array(sorted_data), end_time - start_time

def generate_random_data(n):
    # Generar datos con una distribución más uniforme
    return np.random.randint(1, 10000, size=n, dtype=np.int32)

def parallel_quicksort():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # El proceso root genera los datos
    if rank == 0:
        n = 5
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
        return np.array(final_sorted, dtype=np.int32), original_data
    return None

def print_performance_metrics(parallel_time, sequential_time, n, size):
    speedup = sequential_time / parallel_time
    efficiency = (speedup / size) * 100
    
    print("\n" + "="*50)
    print("MÉTRICAS DE RENDIMIENTO")
    print("="*50)
    print(f"Tamaño del array: {n:,} elementos")
    print(f"Número de procesos: {size}")
    print("-"*50)
    print(f"Tiempo secuencial: {sequential_time*1000:.2f} ms")
    print(f"Tiempo paralelo: {parallel_time*1000:.2f} ms")
    print(f"Speedup: {speedup:.2f}x")
    print(f"Eficiencia: {efficiency:.2f}%")
    
def verify_sorting(original, sorted_data):
    print("\n" + "="*50)
    print("VERIFICACIÓN DE ORDENAMIENTO")
    print("="*50)
    
    # Estadísticas de los datos
    print("Estadísticas:")
    print(f"Valor mínimo: {sorted_data[0]}")
    print(f"Valor máximo: {sorted_data[-1]}")
    print(f"Mediana: {sorted_data[len(sorted_data)//2]}")
    
    print("\nMuestra de datos:")
    print("Primeros 5 elementos:")
    print(f"Original: {original[:5].tolist()}")
    print(f"Ordenado: {sorted_data[:5].tolist()}")
    print("\nÚltimos 5 elementos:")
    print(f"Original: {original[-5:].tolist()}")
    print(f"Ordenado: {sorted_data[-5:].tolist()}")
    
    # Verificaciones
    print("\nVerificaciones:")
    is_sorted = all(sorted_data[i] <= sorted_data[i+1] for i in range(len(sorted_data)-1))
    print(f"¿Array ordenado correctamente?: {is_sorted}")
    
    original_freq = Counter(original)
    sorted_freq = Counter(sorted_data)
    elements_preserved = original_freq == sorted_freq
    print(f"¿Se preservaron todos los elementos?: {elements_preserved}")

if __name__ == "__main__":
    # Tiempo paralelo
    start_time = MPI.Wtime()
    result = parallel_quicksort()
    
    comm = MPI.COMM_WORLD
    if comm.Get_rank() == 0:
        sorted_data, original_data = result
        parallel_time = MPI.Wtime() - start_time
        
        # Tiempo secuencial
        _, sequential_time = sequential_quicksort(original_data)
        
        # Mostrar métricas y verificación
        print_performance_metrics(parallel_time, sequential_time, len(sorted_data), comm.Get_size())
        verify_sorting(original_data, sorted_data)