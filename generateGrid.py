import numpy as np

def generateGrid(sizeX, sizeY, ratio):
    return np.random.choice(['x', 'o'], size=(sizeX, sizeY), p=[ratio, 1-ratio])

if __name__=="__main__":
    xSize = 25
    ySize = 25
    ratio = 0.5

    generateGrid(xSize, ySize, ratio)

