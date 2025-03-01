# Añadir este código en fourth_step.py
import numpy as np
from fourth_step import combinar_T_y_M
from third_step import encontrar_emparejamiento_minimo
from second_step import calcular_nodos_impares_MST
from first_step import calcular_MST

def encontrar_circuito_euleriano(H):
    """
    Encuentra un circuito Euleriano en el grafo H usando el algoritmo de Hierholzer.
    """
    # Crear una copia de las aristas para ir eliminándolas
    from collections import defaultdict
    adj = defaultdict(list)
    # Convertir H a lista de adyacencia con índices de arista
    edges = list(zip(H.row, H.col, H.data))
    for u, v, w in edges:
        adj[u].append(v)

    # Verificar que el grafo sea conexo (asumimos que H es conexo por construcción)
    circuito = []
    pila = []
    nodo_actual = next(iter(adj.keys()))  # Empezar en un nodo con aristas

    pila.append(nodo_actual)

    while pila:
        if adj[nodo_actual]:
            siguiente_nodo = adj[nodo_actual].pop()
            adj[siguiente_nodo].remove(nodo_actual)  # Eliminar arista inversa
            pila.append(nodo_actual)
            nodo_actual = siguiente_nodo
        else:
            circuito.append(nodo_actual)
            nodo_actual = pila.pop()

    circuito.append(nodo_actual)  # Añadir el último nodo
    circuito.reverse()  # Invertir para obtener el orden correcto

    return circuito

if __name__ == "__main__":
    # ...
    instancia = "instances/ulysses22.tsp"
    mst_coo, _, coordenadas = calcular_MST(instancia)
    emparejamiento, _ = encontrar_emparejamiento_minimo(instancia)
    nodos_impares, _ = calcular_nodos_impares_MST(instancia)
    num_nodos = coordenadas.shape[0]
    try:
        H = combinar_T_y_M(mst_coo, emparejamiento, num_nodos, nodos_impares, coordenadas)
        print("Multigrafo H creado exitosamente")
        #graficar_multigrafo(H, coordenadas, emparejamiento)

        # Generar circuito Euleriano
        circuito = encontrar_circuito_euleriano(H)
        print("\nCiclo Eureliano:")
        print(" -> ".join(map(str, circuito)))

    except Exception as e:
        print(f"Error: {str(e)}")
