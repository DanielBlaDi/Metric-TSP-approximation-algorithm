import numpy as np
from scipy.sparse import coo_matrix
from first_step import calcular_MST
def calcular_nodos_impares_MST(instancia):
    """
    calculas los nodos de grado impar del MST
    """
    calculo_MST = calcular_MST(instancia)
    mst:coo_matrix = calculo_MST[0]
    matriz_dispersa_grafo:coo_matrix = calculo_MST[1]

    # Con la matriz de adyacencia del MST, obtengo filas y columnas para ver
    # la cantidad de veces que aparece cada nodo, y asi poder determinar si posee
    # un grado impar de aristas = (cantidad total aristas % 2 != 0)
    # aqui el chiste es unir filas y columnas y contar la cantidad total de apariciones del nodo
    # el cual lo dan las coordenadas (i, j) de la matriz, por que se busca la cantidad total de apariciones?
    # debido a que cada vez que aparezca indicara la existencia de 1 arista ya que siempre las aristas salen de un nodo y acaban en otro
    # y al ser no dirigido (i, j) = (j, i) no va a afectar al conteo de nodos pares he impares

    filas = mst.row # array filas de cada arista
    columnas = mst.col # array columnas de cada arista
    datos = mst.data # array pesos de cada arista

    # Permitira unir las filas y columnas en un solo array

    combinacion_fil_col = np.concatenate((filas, columnas))

    # Nos permitira contar la cantidad total de apariciones de cada nodo, es decir, el grado de estos
    # de una manera mas eficiente y menos costosa que si usaramos dicts (o eso creeria yo, ya que numpy es eficiente para
    # grande volumenes de datos)
    # Tiene dos salidas al marcar true return_counts, la primera nos dira los nodos unicos de MST
    # la segunda nos dira la cantidad de veces que aparece (su grado)


    nodo, grado = np.unique(combinacion_fil_col, return_counts = True)

    # Usa np.where para almacenar en un array los indices de los nodos de grado impar
    # Dado que los nodos estan ordenados ascendentemente, su indice coincide con el que
    # arroja np.where
    grado_impar = np.where(grado % 2 != 0)
    
    # Dado que los indices que arroja np.where coincide con los de nodo
    # podemos hacer nodo[grado_impar], para almacenar cada elemento del array nodo
    # presente en cada uno de los indices que indica grado_par

    nodos_grado_impar = nodo[grado_impar]

    return nodos_grado_impar, matriz_dispersa_grafo

 
if __name__ == "__main__":
    instancia = "instances/prueba.tsp"
    nodos_i, grafo = calcular_nodos_impares_MST(instancia)
    print(nodos_i)
    print(grafo)