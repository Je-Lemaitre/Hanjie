import itertools


# def checkLabel(grid):

#     labelsX = []
#     labelsY = []

#     for y in range(len(grid)):
#         crossX = 0
#         labelX = []
#         for x in range(len(grid[0])):
#             crossX+=grid[y][x]=='x'
#             if crossX>0 and (grid[y][x]!='x' or x == len(grid[0])-1):
#                 labelX.append(crossX)
#                 crossX = 0
#         if not labelX: labelX.append(0)
#         labelsX.append(labelX)

#     for x in range(len(grid[0])):
#         crossY = 0
#         labelY = []
#         for y in range(len(grid)):
#             crossY+=grid[y][x]=='x'
#             if crossY > 0 and (grid[y][x]!='x' or y == len(grid)-1):
#                 labelY.append(crossY)
#                 crossY = 0
#         if not labelY: labelY.append(0)
#         labelsY.append(labelY)
#     return labelsX, labelsY
    
def process_line(line):
    return [sum(1 for _ in group) for key, group in itertools.groupby(line) if key == 'x'] or [0]

def checkLabel(grid):
    labelsX = [process_line(row) for row in grid]
    labelsY = [process_line(col) for col in zip(*grid)]
    return labelsX, labelsY
