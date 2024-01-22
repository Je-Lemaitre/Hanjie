import tkinter as tk
from tkinter import ttk

# Ronan GEAY

MIN_SIZE = 5
MAX_SIZE_WIDTH = 25
MAX_SIZE_HEIGHT = 15

DEFAULT_WIDTH = 5
DEFAULT_HEIGHT = 5

# Grid size according level

EASY_GRID_SIZE = 5
MEDIUM_GRID_SIZE = 10
DIFFICULT_GRID_SIZE = 15
HARD_GRID_SIZE = 25


class GridBoardSelectionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Grid board selection")
        self.width = 5
        self.height = 5


        """
        Frame declaration
        """
        frame_width = ttk.Frame(self, padding="10")
        frame_width.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frame_height = ttk.Frame(self, padding="10")
        frame_height.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        frame_tableau = ttk.Frame(self, padding="10")
        frame_tableau.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        frame_radio = ttk.Frame(self, padding="10")
        frame_radio.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

        frame_validate = ttk.Frame(self, padding="10")
        frame_validate.grid(row=2, column=0, padx=10, pady=10, sticky="ne")

        frame_exit = ttk.Frame(self, padding="10")
        frame_exit.grid(row=2, column=1, padx=10, pady=10, sticky="ne")

        self.canvas = tk.Canvas(frame_tableau, width=249, height=149, borderwidth=1, relief="solid")
        self.canvas.pack()

        label_width = ttk.Label(frame_width, text="Height:")
        label_width.grid(row=1, column=0, pady=(0, 5))

        self.label_value_height = ttk.Label(frame_height, text=str(DEFAULT_HEIGHT))
        self.label_value_height.grid(row=3, column=0)

        self.scale2 = ttk.Scale(frame_height, from_=MIN_SIZE, to=MAX_SIZE_WIDTH, orient="horizontal",
                                command=self.update_label_height)
        self.scale2.grid(row=1, column=0, pady=(0, 5))
        self.scale2.set(DEFAULT_HEIGHT)

        label_height = ttk.Label(frame_height, text="Width:")
        label_height.grid(row=2, column=0, pady=(0, 5))

        self.label_value_width = ttk.Label(frame_width, text=str(DEFAULT_WIDTH))
        self.label_value_width.grid(row=2, column=0)

        self.scale1 = ttk.Scale(frame_width, from_=MIN_SIZE, to=MAX_SIZE_HEIGHT, orient="horizontal",
                                command=self.update_label_width)
        self.scale1.grid(row=0, column=0, pady=(0, 5))
        self.scale1.set(DEFAULT_WIDTH)

        ttk.Label(frame_radio, text="Size of grid according difficulties").pack()

        self.radio_var = tk.StringVar()
        radio1 = ttk.Radiobutton(frame_radio, text="Easy", variable=self.radio_var, value="Easy",
                                 command=self.set_cursors_value)
        radio1.pack(anchor="w")

        radio2 = ttk.Radiobutton(frame_radio, text="Medium", variable=self.radio_var, value="Medium",
                                 command=self.set_cursors_value)
        radio2.pack(anchor="w")

        radio3 = ttk.Radiobutton(frame_radio, text="Difficult", variable=self.radio_var, value="Difficult",
                                 command=self.set_cursors_value)
        radio3.pack(anchor="w")

        radio4 = ttk.Radiobutton(frame_radio, text="Hard", variable=self.radio_var, value="Hard",
                                 command=self.set_cursors_value)
        radio4.pack(anchor="w")

        validate_button = tk.Button(frame_validate, text="Validate", command=self.validate_gridSize, width=20, height=2)
        validate_button.pack(pady=10)

        cancel_button = tk.Button(frame_exit, text="Cancel", command=self.cancel_gridSize, width=20, height=2)
        cancel_button.pack(pady=10)

        self.update_table()

    def update_label_width(self, value):
        value = int(float(value))
        self.label_value_width.config(text=value)
        self.update_table()

    def update_label_height(self, value):
        value = int(float(value))
        self.label_value_height.config(text=value)
        self.update_table()

    def set_cursors_value(self):
        selected_option = self.radio_var.get()

        if selected_option == "Easy":
            self.scale1.set(EASY_GRID_SIZE)
            self.scale2.set(EASY_GRID_SIZE)
        elif selected_option == "Medium":
            self.scale1.set(MEDIUM_GRID_SIZE)
            self.scale2.set(MEDIUM_GRID_SIZE)
        elif selected_option == "Difficult":
            self.scale1.set(DIFFICULT_GRID_SIZE)
            self.scale2.set(DIFFICULT_GRID_SIZE)
        elif selected_option == "Hard":
            self.scale1.set(HARD_GRID_SIZE)
            self.scale2.set(HARD_GRID_SIZE)

        rows = int(self.scale1.get())
        columns = int(self.scale2.get())

        print(f"rows : {rows} and columns : {columns}")

        self.label_value_height.config(text=str(int(self.scale1.get())))
        self.label_value_width.config(text=str(int(self.scale2.get())))
        self.update_table()

    def update_table(self):
        self.canvas.delete("all")

        rows = int(self.scale1.get())
        columns = int(self.scale2.get())

        # print(f"rows : {rows} and columns : {columns}")

        cell_width = 10
        cell_height = 10

        for i in range(1, columns + 1):
            x = i * cell_width
            self.canvas.create_line(x, 0, x, rows * 10, fill="black")

        for i in range(1, rows + 1):
            y = i * cell_height
            self.canvas.create_line(0, y, columns * 10, y, fill="black")

    def cancel_gridSize(self):
        self.destroy()

    def validate_gridSize(self):
        self.height = int(self.scale1.get())
        self.width = int(self.scale2.get())
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GridBoardSelectionWindow(root)
    root.mainloop()