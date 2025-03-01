from first_step import calcular_MST
from second_step import calcular_nodos_impares_MST
from third_step import encontrar_emparejamiento_minimo
from fourth_step import combinar_T_y_M
from fifth_step import encontrar_circuito_euleriano

def aplicar_shortcutting(circuito):
    """
    Aplica el shortcutting al circuito Euleriano para obtener un ciclo Hamiltoniano.
    """
    visitados = set()
    ciclo_hamiltoniano = []
    for nodo in circuito:
        if nodo not in visitados:
            ciclo_hamiltoniano.append(nodo)
            visitados.add(nodo)
    # Cerrar el ciclo añadiendo el primer nodo al final
    if ciclo_hamiltoniano:
        ciclo_hamiltoniano.append(ciclo_hamiltoniano[0])
    return ciclo_hamiltoniano

if __name__ == "__main__":
    # ...
    instancia = "instances/pla85900.tsp"
    mst_coo, _, coordenadas = calcular_MST(instancia)
    emparejamiento, _ = encontrar_emparejamiento_minimo(instancia)
    nodos_impares, _ = calcular_nodos_impares_MST(instancia)
    num_nodos = coordenadas.shape[0]
    try:
        H = combinar_T_y_M(mst_coo, emparejamiento, num_nodos, nodos_impares, coordenadas)
        #graficar_multigrafo(H, coordenadas, emparejamiento)

        # Generar circuito Euleriano
        circuito = encontrar_circuito_euleriano(H)

        # Aplicar shortcutting para obtener el ciclo Hamiltoniano
        ciclo_hamiltoniano = aplicar_shortcutting(circuito)
        print("\nCiclo Hamiltoniano después del shortcutting:")
        print(" -> ".join(map(str, ciclo_hamiltoniano)))

    except Exception as e:
        print(f"Error: {str(e)}")
