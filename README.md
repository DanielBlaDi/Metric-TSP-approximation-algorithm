# Metric-TSP-approximation-algorithm
Here is the space where we are gonna try to create a scirpt that can solve some instances pf the Metric-TSP

## How to run

### With poetry

Obviusly `poetry` must be [installed](https://python-poetry.org/docs/#installation),  install dependencies using:

```shell
$ poetry install
```

Then, run it using:
```shell
$ poetry run python metric-TSP/main.py ./instances/your_instance.tsp

// For pla85900 use:
$ poetry run python metric-TSP/main.py ./instances/pla85900.tsp
```

### Without poetry

#### Dependencies:

- python3
- matplotlib
- networkx
- numpy
- scipy

Then, run it using:
```shell
$ python metric-TSP/main.py ./instances/your_instance.tsp

// For pla85900 use:
$ python metric-TSP/main.py ./instances/pla85900.tsp
```

## Step by step

You can exexute until x step by running that step.py file, if you want to change the instance edit variable `instancia` in the file.
