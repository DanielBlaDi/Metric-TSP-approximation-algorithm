import numpy as np
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
import networkx as nx
from first_step import calcular_MST
from third_step import encontrar_emparejamiento_minimo
from second_step import calcular_nodos_impares_MST

def combinar_T_y_M(mst_coo, emparejamiento, num_nodos, nodos_impares, coordenadas):
    """
    Combina el MST y el emparejamiento, calculando las distancias desde las coordenadas.
    """
    # Validar emparejamiento cubre todos los nodos impares
    nodos_emparejados = set()
    for u, v in emparejamiento:
        nodos_emparejados.add(u)
        nodos_emparejados.add(v)
    if len(nodos_emparejados) != len(nodos_impares):
        raise ValueError("Emparejamiento no cubre todos los nodos impares.")

    # Obtener aristas del MST (ya incluyen ambas direcciones y pesos reales)
    filas_T = np.concatenate([mst_coo.row, mst_coo.col])
    columnas_T = np.concatenate([mst_coo.col, mst_coo.row])
    pesos_T = np.concatenate([mst_coo.data, mst_coo.data])

    # Calcular pesos del emparejamiento desde coordenadas
    filas_M, columnas_M, pesos_M = [], [], []
    for u, v in emparejamiento:
        distancia = np.linalg.norm(coordenadas[u] - coordenadas[v])  # Distancia Euclidiana
        filas_M.extend([u, v])
        columnas_M.extend([v, u])
        pesos_M.extend([distancia, distancia])  # Ambas direcciones

    # Combinar todas las aristas
    filas_H = np.concatenate([filas_T, filas_M])
    columnas_H = np.concatenate([columnas_T, columnas_M])
    pesos_H = np.concatenate([pesos_T, pesos_M])

    # Construir H con pesos reales
    H_real = coo_matrix((pesos_H, (filas_H, columnas_H)), shape=(num_nodos, num_nodos))

    # Validar grados pares (usar matriz binaria)
    H_bin = coo_matrix((np.ones_like(pesos_H), (filas_H, columnas_H)), shape=(num_nodos, num_nodos))
    grados = H_bin.sum(axis=0).A1
    if not np.all(grados % 2 == 0):
        raise ValueError(f"Nodos con grado impar: {np.where(grados % 2 != 0)[0]}")

    return H_real



if __name__ == "__main__":
    instancia = "instances/ulysses22.tsp"
    mst_coo, _, coordenadas = calcular_MST(instancia)
    emparejamiento, _ = encontrar_emparejamiento_minimo(instancia)
    nodos_impares, _ = calcular_nodos_impares_MST(instancia)
    num_nodos = coordenadas.shape[0]

    try:
        H = combinar_T_y_M(mst_coo, emparejamiento, num_nodos, nodos_impares, coordenadas)
        print("Multigrafo H creado exitosamente")
        
    except Exception as e:
        print(f"Error: {str(e)}")