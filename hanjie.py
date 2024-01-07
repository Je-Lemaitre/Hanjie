from generateGrid import generateGrid
from checkLabel import checkLabel
from display import display
from binarise import binarise
from loadImage import loadImage

def start_game(difficulty,gridSize, img):
    grid = generateGrid(gridSize)
    labelsX, labelsY = checkLabel(grid)
    display(grid, labelsX, labelsY)
    binarise(img)
    return 42

if __name__ == "__main__":
    #grid = generateGrid()

    path = loadImage()
    grid = binarise(path)
    # Further processing with the resized image can be done here
    #grid = binarise('pictures/mickey.jpg')
    #grid = binarise('pictures/zelda_1.jpg')
    #grid = binarise('pictures/panda.webp')
    #grid = binarise('pictures/EffeilTower.png')
    #grid = binarise('pictures/taz_300_300.jpg')

    labelsX, labelsY = checkLabel(grid)

    for row in grid: print(row)
    display(grid, labelsX, labelsY, 1)

