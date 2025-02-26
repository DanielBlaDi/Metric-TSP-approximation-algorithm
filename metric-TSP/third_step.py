import numpy as np
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment
from second_step import calcular_nodos_impares_MST
from first_step import calcular_MST

def encontrar_emparejamiento_minimo(instancia):
    # Obtener MST y coordenadas
    mst_coo, _, coordenadas = calcular_MST(instancia)
    
    # Identificar nodos impares y validar paridad
    nodos_impares, _ = calcular_nodos_impares_MST(instancia)
    nodos_impares = np.array(nodos_impares, dtype=int)
    if len(nodos_impares) % 2 != 0:
        raise ValueError("Número impar de nodos impares. No se puede emparejar.")
    
    # Construir matriz de distancias
    coordenadas_impares = coordenadas[nodos_impares]
    matriz_distancias = distance_matrix(coordenadas_impares, coordenadas_impares)
    np.fill_diagonal(matriz_distancias, np.inf) # Evita auto-emparejamientos (nodo consigo mismo) al asignar costo infinito en la diagonal.
    
    # Obtener emparejamiento con linear_sum_assignment
    row_ind, col_ind = linear_sum_assignment(matriz_distancias)
    
    # Procesar pares y asegurar cobertura total
    emparejamiento = []
    unpaired = set(nodos_impares.tolist())
    
    for row, col in zip(row_ind, col_ind):
        u = nodos_impares[row]
        v = nodos_impares[col]
        if u == v:
            continue  # Ignorar pares (i, i)
        if u in unpaired and v in unpaired:
            sorted_pair = tuple(sorted((u, v)))
            emparejamiento.append(sorted_pair)
            unpaired.discard(u)
            unpaired.discard(v)
    
    # Emparejar nodos restantes (si los hay)
    while unpaired:
        u = unpaired.pop()
        v = unpaired.pop()
        emparejamiento.append(tuple(sorted((u, v))))
    
    # Calcular peso total usando coordenadas originales
    peso_total = sum(np.linalg.norm(coordenadas[u] - coordenadas[v]) for u, v in emparejamiento)
    
    return emparejamiento, peso_total

if __name__ == "__main__":
    instancia = "instances/ulysses22.tsp"
    emparejamiento, peso_total = encontrar_emparejamiento_minimo(instancia)
    print(f"Emparejamiento mínimo: {emparejamiento}")
    print(f"Peso total: {peso_total:.2f}")