import sys

from first_step import calcular_MST
from second_step import calcular_nodos_impares_MST
from third_step import encontrar_emparejamiento_minimo
from fourth_step import combinar_T_y_M
from fifth_step import encontrar_circuito_euleriano
from sixth_step import aplicar_shortcutting

if len(sys.argv) < 2:
    print('Por favor pasar la direccion a la instancia como primer argumento')
    sys.exit(1)

instance_path = sys.argv[1]


try:
    mst_coo, _, coordenadas = calcular_MST(instance_path)
    emparejamiento, _ = encontrar_emparejamiento_minimo(instance_path)
    nodos_impares, _ = calcular_nodos_impares_MST(instance_path)
    num_nodos = coordenadas.shape[0]

    H = combinar_T_y_M(mst_coo, emparejamiento, num_nodos, nodos_impares, coordenadas)
    #graficar_multigrafo(H, coordenadas, emparejamiento)

    # Generar circuito Euleriano
    circuito = encontrar_circuito_euleriano(H)

    # Aplicar shortcutting para obtener el ciclo Hamiltoniano
    ciclo_hamiltoniano = aplicar_shortcutting(circuito)
    print("\nSolucion:")
    print(" -> ".join(map(str, ciclo_hamiltoniano)))

except Exception as e:
    print(f"Error: {str(e)}")
