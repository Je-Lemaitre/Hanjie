from generateGrid import generateGrid
from checkLabel import checkLabel
from display import display
from binarise import binarise

def start_game(difficulty,gridSize, img):
    grid = generateGrid(gridSize)
    labelsX, labelsY = checkLabel(grid)
    display(grid, labelsX, labelsY)
    binarise(img)
    return 42

if __name__ == "__main__":
    grid = generateGrid()
    labelsX, labelsY = checkLabel(grid)
    display(grid, labelsX, labelsY)
    binarise()