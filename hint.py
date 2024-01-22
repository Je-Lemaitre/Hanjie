import random
import tkinter as tk

# Return one case not found yet
def hint_position(grid, player_cases):
    correct_positions = grid_to_positions(grid)
    player_positions = grid_to_positions(player_cases)

    incorrect_positions = [position for position in player_positions if position not in correct_positions]
    if(len(incorrect_positions)>0):
        random_hint = random.choice(incorrect_positions)
        return random_hint, True

    possible_hints = [position for position in correct_positions if position not in player_positions]
    if len(possible_hints) > 0:  # If at least one correct square is not found
        random_hint = random.choice(possible_hints)
        return random_hint, False
    else:
        return []

# Return a list with all the positions of the squares to find
def grid_to_positions(grid):
    positions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'x':
                positions.append([j, i])
    return positions

def handle_hint_click(cases, grid, buttons):
    hint = hint_position(grid, cases)
    #vérifier que hint est de la forme [x,y]
    if len(hint) == 0:
        return
    else :
        button = buttons[hint[1]][hint[0]]
        button.config(activebackground="green")
        button.config(bg="green")