import numpy as np
from scipy.sparse import coo_matrix
from first_step import calcular_MST
def calcular_nodos_impares_MST(instancia):
    mst:coo_matrix = calcular_MST(instancia)
    
