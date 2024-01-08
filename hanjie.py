from generateGrid import generateGrid
from checkLabel import checkLabel
from display import display
from loadImage import loadImage
from binarise import binarise

if __name__ == "__main__":
    #grid = generateGrid()

    path = loadImage()
    grid = binarise(path)
    #grid = binarise('pictures/mickey.jpg')
    #grid = binarise('pictures/zelda_1.jpg')
    #grid = binarise('pictures/panda.webp')
    #grid = binarise('pictures/EffeilTower.png')
    #grid = binarise('pictures/taz_300_300.jpg')

    labelsX, labelsY = checkLabel(grid)
    for row in grid: print(row)
    display(grid, labelsX, labelsY, 1)