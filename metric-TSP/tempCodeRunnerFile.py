import numpy as np
from scipy.spatial import distance_matrix 
from scipy.optimize import linear_sum_assignment
from second_step import calcular_nodos_impares_MST
from first_step import calcular_MST

def encontrar_emparejamiento_minimo(instancia):
    #Obtener MST y las coordenadas
    mst_coo, matriz_dispersa_coo, coordenadas = calcular_MST(instancia)
    #Identificar los nodos impares
    nodos_impares, _ = calcular_nodos_impares_MST(instancia)  
    nodos_impares = np.array(nodos_impares, dtype=int)  

    #Calcula la matriz de distancias sin construir un grafo completo
    coordenadas_impares = coordenadas[nodos_impares]
    matriz_distancias = distance_matrix(coordenadas_impares, coordenadas_impares)
    np.fill_diagonal(matriz_distancias, np.inf) #Evita que el algoritmo de asignación seleccione pares (i, i), que son inválidos.

    #Resuelve el emparejamiento mínimo usando el algoritmo de asignación
    row_ind, col_ind = linear_sum_assignment(matriz_distancias)

    # Crea pares de emparejamiento
    emparejamiento = []
    seen = set()
    '''
    En un grafo no dirigido, las aristas (u, v) y (v, u) representan la misma conexión. 
    Si el algoritmo de emparejamiento genera ambas, estarías añadiendo aristas duplicadas.
    '''
    for row, col in zip(row_ind, col_ind):
        u = nodos_impares[row]
        v = nodos_impares[col]
        if u != v:  # Ignorar pares (i, i) por si acaso
            sorted_pair = tuple(sorted((u, v)))
            if sorted_pair not in seen:
                emparejamiento.append((u, v))
                seen.add(sorted_pair)

    peso_total = matriz_distancias[row_ind, col_ind].sum()

    return emparejamiento, peso_total

# Ejemplo de uso
if __name__ == "__main__":
    instancia = "instances/ulysses22.tsp"
    emparejamiento, peso_total = encontrar_emparejamiento_minimo(instancia)
    print("Emparejamiento:", emparejamiento)
    print("Peso total:", peso_total)