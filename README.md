# Algoritmo de aproximacion del TSP Metrico
Esta es una implementacion del algoritmo de christofides para poder resolver algunas instancias del TSP Metrico extraido de TSPLIB

## Como correrlo

### Con poetry

`poetry` debe estar [instalado](https://python-poetry.org/docs/#installation),  para instalar las dependencias con poetry utiliza:

```shell
$ poetry install
```

Luego, correlo de la siguiente manera:
```shell
$ poetry run python metric-TSP/main.py ./instances/your_instance.tsp

// For pla85900 use:
$ poetry run python metric-TSP/main.py ./instances/pla85900.tsp
```

### Sin poetry:

#### Dependencias:

- python3
- matplotlib
- networkx
- numpy
- scipy

Luego correlo usando:
```shell
$ python metric-TSP/main.py ./instances/your_instance.tsp

// For pla85900 use:
$ python metric-TSP/main.py ./instances/pla85900.tsp
```

## Paso a paso

Los pasos se ejecutan de manera secuencial, puedes ejecutar el script hasta determinado paso indicando el ultimo paso file.py a ejecutar, es decir, si deseas ejecutar paso 1, paso 2 y paso 3, tendras que ejecutar el archivo del paso tres (third_step.py), si deseas cambiar la instancia puedes hacerlo cambiando la variable `instancia` en el archivo, tomando en cuenta las instancias cargadas en el directorio `instances`.
