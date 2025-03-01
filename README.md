# Metric-TSP-approximation-algorithm
Here is the space where we are gonna try to create a scirpt that can solve some instances pf the Metric-TSP

## How to run

By default, it solves the pla85900.tsp problem, you can change it by modifying the variable `instacia` in the step you want to run (sixth for solution), for one of the instaces of the problem in the `instances/` directory.

### With poetry

Obviusly `poetry` must be [installed](https://python-poetry.org/docs/#installation),  install dependencies using:

```shell
$ poetry install
```

Then, run it using:
```shell
$ poetry run python metric-TSP/sixth_step.py
```

### Without poetry

#### Dependencies:

- python3
- matplotlib
- networkx
- numpy
- scipy

Then run it using:
```shell
$ python metric-TSP/sixth_step.py
```
