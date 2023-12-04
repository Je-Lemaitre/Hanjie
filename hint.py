import random
import tkinter as tk


# Return one case not found yet
def hint_position(grid, player_cases):
    correct_positions = grid_to_positions(grid)
    player_positions = grid_to_positions(player_cases)
    possible_hints = [position for position in correct_positions if position not in player_positions]
    if len(possible_hints) > 0:  # If at lest one correct square is not found
        random_hint = random.choice(possible_hints)
        return random_hint
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


def hint_button(window, cases, grid, buttons):
    button = tk.Button(window, text="Hint", width=3, height=3,
                       bg="light gray", highlightthickness=2, highlightcolor="white",
                       activebackground="light gray")
    return button
