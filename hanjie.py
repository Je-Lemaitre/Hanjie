from generateGrid import generateGrid
from checkLabel import checkLabel
from display import display
from binarise import binarise

if __name__ == "__main__":
    grid = generateGrid()
    labelsX, labelsY = checkLabel(grid)
    display(grid, labelsX, labelsY)
    binarise()