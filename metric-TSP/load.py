import numpy as np
import time

def cargar_coordenadas_tsp(ruta_archivo):
    coordenadas = []
    tipo = None
    with open(ruta_archivo, 'r') as archivo:
        # Recorre el archivo hasta encontrar la línea NODE_COORD_SECTION
        while True:
            linea = archivo.readline()
            if "EDGE_WEIGHT_TYPE: GEO" in linea:
                tipo = "GEO"
            elif "EDGE_WEIGHT_TYPE : EUC_2D" in linea or "EDGE_WEIGHT_TYPE : CEIL_2D" in linea:
                tipo = "EUC"
            if "NODE_COORD_SECTION" in linea:
                break

        # Lee las coordenadas, sin tomar en cuenta el primer valor que es el que indica su posicion (id)
        # Se detiene al encontrar la EOF o cuando no haya linea siguiente
        while True:
            linea = archivo.readline()
            if "EOF" in linea or not linea:
                break
            partes = linea.strip().split()
            if len(partes) == 3:  # Se asegurara de que la línea tenga 3 partes (id, x/latitud, y/longitud)
                _, x, y = partes
                coordenadas.append((float(x), float(y)))

    # Convierte en array las coordenadas para que numpy realice las operaciones facilmente sobre ellas
    coordenadas = np.array(coordenadas)
    return coordenadas, tipo

if __name__ == "__main__":
    # Ejemplo de uso
    ruta = input("Ingrese el nombre de la instancia: ")
    inicio = time.time()
    coordenadas = cargar_coordenadas_tsp("instances/" + ruta)
    fin = time.time()
    resultado = fin - inicio
    print(f"Tiempo carga: {resultado:.6f}")
    print("Coordenadas cargadas:")
    print(coordenadas[1])