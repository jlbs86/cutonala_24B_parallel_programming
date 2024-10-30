import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Generar puntos aleatorios en el proceso raíz
if rank == 0:
    points = np.random.rand(100, 2)
else:
    points = None

# Broadcasting de los puntos a todos los procesos
points = comm.bcast(points, root=0)

# Dividir los puntos en subconjuntos
points_split = np.array_split(points, size)

# Cada proceso trabaja con su subconjunto de puntos
local_points = points_split[rank]

# Calcular la triangulación localmente
local_tri = Delaunay(local_points)

# Recopilar los resultados en el proceso raíz
local_tris = comm.gather(local_tri, root=0)

if rank == 0:
    # Combinar las triangulaciones locales
    all_points = np.vstack([tri.points for tri in local_tris])
    global_tri = Delaunay(all_points)

    # Plotear la triangulación global
    plt.triplot(global_tri.points[:,0], global_tri.points[:,1], global_tri.simplices)
    plt.plot(global_tri.points[:,0], global_tri.points[:,1], 'o')
    plt.savefig('/content/delaunay_triangulation__collective_communication_broadcast.png')  # Guardar la gráfica
