import numpy as np
from scipy.spatial import Delaunay
from scipy.sparse import coo_matrix
#, csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import load

def calcular_MST(instancia):
    coordenadas = load.cargar_coordenadas_tsp(instancia)[0]
    tipo = load.cargar_coordenadas_tsp(instancia)[1] # Tipo se usaria para instancias Geo que requieren un caculo especial de distancias
    numero_coordenadas = coordenadas.shape[0] # Shape retorna una tupla (# filas, # columnas) de un array de numpy
    
    if tipo == "GEO":
        coordenadas = geo_to_euc(coordenadas)

    # Calcula la triangulacion de Delaunay sobre la lista de coordenadas, retorna una matriz donde cada fila
    # contiene 3 datos que hacen referencia a los indices de las coordenadas que conforman los triangulos
    # ej: [[coord1, coord2, coord3], [coord1, coord2, coord4]]

    triangulacion = Delaunay(coordenadas) 

    aristas = set()
    
    # Recorre la matriz generada por "Delaunay(coordenadas)" y almacena en un set todas las aristas
    # Ya que una arista puede estar presente en mas de 1 triangulo
    # se utiliza un set para almacenar las aristas sin repetirlas

    for simplex in triangulacion.simplices:
        simplex = sorted(simplex)
        aristas.add((simplex[0], simplex[1]))
        aristas.add((simplex[1], simplex[2]))
        aristas.add((simplex[0], simplex[2]))
    aristas = list(aristas)

    filas = [i for i, j in aristas] + [j for i, j in aristas]  # Filas (i_n, j_m) (al ser un grafo no dirigido (i_n, j_n) = (j_m, i_m))
    columnas = [j for i, j in aristas] + [i for i, j in aristas]  # Columnas (j_n, i_m) (al ser un grafo no dirigido (i_n, j_n) = (j_m, i_m))

    # Pesos (distancia de cada arista entre cada nodo i, j)
    # Ya que es un grafo no dirigido, (i, j) = (j, i) y por ende comparten los mismos pesos,
    # teniendo los pesos de (j, i) se multiplica por 2, para asi obtener el mismo peso para (j, i)
    # np.linalg.norm calcula la norma de un vector, para conocer la distancia entre i y j 
    # se normaliza (i - j) y se usa la funcion de numpy para la norma del vector resultante

    pesos = [round(np.linalg.norm(coordenadas[i] - coordenadas[j]), 2) for i, j in aristas] * 2

    # Crea la matriz dispersa en formato COO (COOrdinate format) en base a las variables columnas, filas y pesos.
    # Matriz dispersa unicamente almacena aristas no nulas, es decir donde el peso de estas
    # valga 0 dado que no existe una arista entre A y B, ocupa menos espacio en memoria que una matriz densa (almacena los 0)
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html#scipy.sparse.coo_matrix

    matriz_dispersa_coo = coo_matrix((pesos, (filas, columnas)), shape=(numero_coordenadas, numero_coordenadas))

    # Pasa a formato csr ya que este formato es mas eficiente para 
    # operaciones matriciales y resulta mas efectivo para poder usar minimum_spanning_tree()
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_array.html#scipy.sparse.csr_array

    matriz_dispersa_csr = matriz_dispersa_coo.tocsr()

    # Se llama la funcion arbol de expansion minima la cual
    # retorna una matriz en formato csr con la matriz dispersa de adyacencia del MST
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.minimum_spanning_tree.html#scipy.sparse.csgraph.minimum_spanning_tree

    mst = minimum_spanning_tree(matriz_dispersa_csr)

    # Se vuelve a pasar a formato coo para poder extraer facilmente la matriz de adyacencia para
    # Pasos posteriores
    mst_coo = mst.tocoo()

    return mst_coo, matriz_dispersa_coo,coordenadas


def geo_to_euc(geo_coords):
    """
    Dadas unas coordenadas en formato geografico (latitud y longitud), realiza la 
    proyección equirrectangular para pasar a coordenadas bidimensionales y aplicar el
    proceso que se realiza para las demas instancias.
    Es recomendable usarlo para instancias pequeñas, ya que a mayor distancia puede 
    haber un mayor errora la hora de calcular
    las distancias entre ciudades
    
    Formula usada
    https://pubs.usgs.gov/pp/1395/report.pdf#page=103
    lambda0 = 0
    factores h y k no se tomaron en cuenta para pasar a coord euclidianas
    phi1 = latitud promedio
    """

    # Radio aproximado promedio de la Tierra en km = 6371
    # Radio ecuatorial aproximado en km = 6378
    R = 6371.0

    # Np.radians convierte a radianes todos los angulos de una matriz
    # lambda = latitud en radianes
    # phi = longitud en radianes

    # geo_coords[:, 0] -> 
    # : toma todas las filas 
    # 0 toma la primer columna de cada fila (latitud)
    # 1 toma la segunda columna de cada fila (longitud)
    latitudes = np.radians(geo_coords[:, 0])
    longitudes = np.radians(geo_coords[:, 1])

    # Se calcula la latitud promedio con ayuda de np.mean
    lat_mean = np.mean(latitudes)

    # Convertir a coordenadas euclidianas con la formula
    # Se puese hacer R * longitudes ya que seria parecido 
    # a multiplicar un escalar por una matriz
    # podrias usar la funcion math.cos() ya que last_mean es un escalar 
    # pero dado que trabajamos con numpy y solo se usa para eso se decidio usar np.cos()
    x = R * longitudes * np.cos(lat_mean)
    y = R * latitudes

    # Coordenadas euclidianas resultantes
    # Combina en una matriz las listas x, y
    # Ej:
    # x = [x1, x2, x3]
    # y = [y1, y2, y3]
    # euc_coords = [[x1, y1], [x2, y2], [x3, y3]]

    euc_coords = np.column_stack((x, y))

    return euc_coords

if __name__ == "__main__":
    instancia = "instances/prueba.tsp"
    mst, grafo = calcular_MST(instancia)
    
    # matriz_adyacencia_densa = mst.toarray()

    print("Grafo")
    # print(grafo.row)
    # print(grafo.col)
    # print(grafo.data)
    # print()
    print("MST")
    # print(mst.row)
    # print(mst.col)
    # print(mst.data)
    # print()
    # print("MST densa")
    # print(matriz_adyacencia_densa)