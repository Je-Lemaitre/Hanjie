import tkinter as tk
from checkLabel import checkLabel

# Function to handle the click on a case
def handle_case_click(x, y, cases, buttons, labelsX, labelsY, event):

    labelsXInput, labelsYInput = checkLabel(cases)
    if (labelsXInput == labelsX and labelsYInput == labelsY): return

    if event == "left":
        cases[y][x] = "x"
        buttons[y][x].config(activebackground="black")
        buttons[y][x].config(bg="black")

    elif event == "right":
        cases[y][x] = "o"
        buttons[y][x].config(activebackground="yellow")
        buttons[y][x].config(bg="yellow")
    else:
        cases[y][x] = " "
        buttons[y][x].config(activebackground="light gray")
        buttons[y][x].config(bg="light gray")

    labelsXInput, labelsYInput = checkLabel(cases)
    if (labelsXInput == labelsX and labelsYInput == labelsY):
        win = True
        print("YAAAY")

        for i in range(len(buttons)):
            for j in range(len(buttons[i])):
                if(buttons[i][j].cget("activebackground") == "black"):
                    buttons[i][j].config(activebackground="light green")
                    buttons[i][j].config(bg="light green")


# Function to display the GUI
def display(window, grid, labelsX, labelsY, size):

    #Resizing the labels
    sizeLabX = 0
    for labelX in labelsX:
        if(len(labelX)>sizeLabX): sizeLabX=len(labelX)
    sizeLabY = 0
    for labelY in labelsY:
        if(len(labelY)>sizeLabY): sizeLabY=len(labelY)

    sizeX = len(grid[0])
    sizeY = len(grid)

    # Create a 3x3 grid of cases
    cases = [[" " for _ in range(sizeX)] for _ in range(sizeY)]
    buttons = []

    # Create labels for column headers (numbers on top)
    for x in range(sizeX):
        for y in range(len(labelsY[x])):
            label = tk.Label(window, text=str(labelsY[x][len(labelsY[x])-1-y]), width=3*size, height=2*size)
            label.grid(row=sizeLabY-1-y, column=x+sizeLabX)

    # Create labels for row headers (numbers on the left)
    for y in range(sizeY):
        for x in range(len(labelsX[y])):
            label = tk.Label(window, text=str(labelsX[y][len(labelsX[y])-1-x]), width=3*size, height=2*size)
            label.grid(row=y+sizeLabY, column=sizeLabX-1-x)

    # Create buttons for the cases
    for y in range(sizeY):
        row = []
        for x in range(sizeX):
            case_button = tk.Button(window, text=cases[y][x], width=3*size, height=2*size,
                                    bg="light gray", highlightthickness=1*size, highlightcolor="white",
                                    activebackground="light gray")

            # Bind left and right click event handlers to the button
            case_button.bind("<Button-1>", lambda event, x=x, y=y: handle_case_click(x, y, cases, buttons, labelsX, labelsY, "left"))  # Left click
            case_button.bind("<Button-2>", lambda event, x=x, y=y: handle_case_click(x, y, cases, buttons, labelsX, labelsY, "middle"))  # Right click
            case_button.bind("<Button-3>", lambda event, x=x, y=y: handle_case_click(x, y, cases, buttons, labelsX, labelsY, "right"))  # Right click

            case_button.grid(row=y+sizeLabY, column=x+sizeLabX)
            row.append(case_button)
        buttons.append(row)

    for i in range(int((sizeX-1)/5)):
        for j in range(sizeY):
            frame = tk.Frame(window, width=2, height=48, borderwidth=2, relief="solid")
            frame.grid(row=sizeLabY+j, column=4+sizeLabX+i*5, columnspan=2)

    for i in range(int((sizeY-1)/5)):
        for j in range(sizeX):
            frame = tk.Frame(window, width=52, height=2, borderwidth=3, relief="solid")
            frame.grid(row=4+sizeLabY+i*5, column=sizeLabX+j, columnspan=1, sticky="s")

    # Start the Tkinter main loop
    window.mainloop()
