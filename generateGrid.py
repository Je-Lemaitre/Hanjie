import numpy as np

def generateGrid(sizeX: int, sizeY: int, ratio: int):
    grid = np.random.choice(['x', 'o'], size=(sizeY,sizeX), p=[ratio, 1-ratio])
    return grid.tolist()