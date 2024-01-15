import tkinter as tk
from checkLabel import checkLabel
from generateGrid import generateGrid

win = False

# Function to handle the click on a case
def handle_case_click(x, y, cases, buttons, labelsX, labelsY, event):
    event_mapping = {
        "left": ("x", "black", "black"),
        "right": ("o", "yellow", "yellow"),
        "default": (" ", "light gray", "light gray"),
    }
    
    case_value, active_bg, bg = event_mapping.get(event, event_mapping["default"])
    cases[y][x] = case_value
    buttons[y][x].config(activebackground=active_bg, bg=bg)

    labelsXInput, labelsYInput = checkLabel(cases)
    if labelsXInput == labelsX and labelsYInput == labelsY:
        win = True
        print("YAAAY")

# Function to display the GUI
def display(grid, labelsX, labelsY, size):
    sizeLabX = max(len(labelX) for labelX in labelsX)
    sizeLabY = max(len(labelY) for labelY in labelsY)

    sizeX = len(grid[0])
    sizeY = len(grid)

    # Create a Tkinter window
    window = tk.Tk()
    window.title("Hanjie Game")

    # Create a 3x3 grid of cases
    cases = [[" " for _ in range(sizeX)] for _ in range(sizeY)]
    buttons = []

    # Create labels for column headers (numbers on top)
    for x in range(sizeX):
        for y, label_text in enumerate(reversed(labelsY[x])):
            label = tk.Label(window, text=str(label_text), width=1, height=1, borderwidth=0, relief="flat")
            label.grid(row=sizeLabY-1-y, column=x+sizeLabX, ipadx=0, ipady=0, padx=0, pady=0)

    # Create labels for row headers (numbers on the left)
    for y in range(sizeY):
        for x, label_text in enumerate(reversed(labelsX[y])):
            label = tk.Label(window, text=str(label_text), width=1, height=1, borderwidth=0, relief="flat")
            label.grid(row=y+sizeLabY, column=sizeLabX-1-x, ipadx=0, ipady=0, padx=0, pady=0)

    # Create buttons for the cases
    for j in range(sizeY):
        row = []
        for i in range(sizeX):
            case_button = tk.Button(window, text=cases[j][i], bd=0, width=2, height = 1,
                                    bg="light gray", highlightcolor="white",
                                    activebackground="light gray", borderwidth=0, relief="flat")

            # Bind left and right click event handlers to the button
            case_button.bind("<Button-1>", lambda event, x=i, y=j: handle_case_click(i, j, cases, buttons, labelsX, labelsY, "left"))  # Left click
            case_button.bind("<Button-2>", lambda event, x=i, y=j: handle_case_click(i, j, cases, buttons, labelsX, labelsY, "middle"))  # Right click
            case_button.bind("<Button-3>", lambda event, x=i, y=j: handle_case_click(i, j, cases, buttons, labelsX, labelsY, "right"))  # Right click
            case_button.grid(row=j+sizeLabY, column=i+sizeLabX , ipadx = 0, ipady = 0, padx = 0, pady = 0)
            row.append(case_button)
        buttons.append(row)

    for i in range(int((sizeX-1)/5)):
        for j in range(sizeY):
            frame = tk.Frame(window, width=2, height=24, borderwidth=1, relief="solid")
            frame.grid(row=sizeLabY+j, column=4+sizeLabX+i*5, columnspan=2, ipadx = 0, ipady = 0, padx = 0, pady = 0)

    for i in range(int((sizeY-1)/5)):
        for j in range(sizeX):
            frame = tk.Frame(window, width=26, height=2, borderwidth=1, relief="solid")
            frame.grid(row=4+sizeLabY+i*5, column=sizeLabX+j, columnspan=1, sticky="s", ipadx = 0, ipady = 0, padx = 0, pady = 0)

    # Start the Tkinter main loop
    window.mainloop()


if __name__=="__main__":
    xSize = 25
    ySize = 25
    ratio = 0.5

    theGrid = generateGrid(xSize,ySize,ratio)
    theLabelsX, theLabelsY = checkLabel(theGrid)
    display(theGrid, theLabelsX, theLabelsY, 0.5)
