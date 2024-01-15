def checkLabel(grid):

    labelsX = []
    labelsY = []

    for y in range(len(grid)):
        crossX = 0
        labelX = []
        for x in range(len(grid[0])):
            crossX+=grid[y][x]=='x'
            if crossX>0 and (grid[y][x]!='x' or x == len(grid[0])-1):
                labelX.append(crossX)
                crossX = 0
        if(len(labelX)==0): labelX.append(0)
        labelsX.append(labelX)

    for x in range(len(grid[0])):
        crossY = 0
        labelY = []
        for y in range(len(grid)):
            crossY+=grid[y][x]=='x'
            if crossY > 0 and (grid[y][x]!='x' or y == len(grid)-1):
                labelY.append(crossY)
                crossY = 0
        if(len(labelY)==0): labelY.append(0)
        labelsY.append(labelY)
    return labelsX, labelsY