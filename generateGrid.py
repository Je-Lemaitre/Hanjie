import numpy as np

def generateGrid(sizeX, sizeY, ratio):
    grid = np.random.choice(['x', 'o'], size=(sizeX, sizeY), p=[ratio, 1-ratio])
    return grid.tolist()