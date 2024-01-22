import itertools
    
def process_line(line):
    return [sum(1 for _ in group) for key, group in itertools.groupby(line) if key == 'x'] or [0]

def checkLabel(grid):
    labelsX = [process_line(row) for row in grid]
    labelsY = [process_line(col) for col in zip(*grid)]
    return labelsX, labelsY
