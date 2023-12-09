import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Import ImageTk from PIL
from datetime import datetime
#import hanjie
import grid_board_selection as gbs
from os import listdir
from os.path import join
import random as rd


class HanjieHomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hanjie - Puzzle Game")
        self.geometry("800x600")

        # Header with Title and Image
        game_image = Image.open("hanjie_image.png").resize((50, 50))
        self.game_image_tk = ImageTk.PhotoImage(game_image)  # Use ImageTk to convert to Tkinter-compatible format

        header_frame = tk.Frame(self)
        header_frame.pack(pady=20)

        image_label = tk.Label(header_frame, image=self.game_image_tk)  # Use self.game_image_tk here
        image_label.grid(row=0, column=0, padx=10)

        title_label = tk.Label(header_frame, text="Welcome to Hanjie - Puzzle Game", font=("Helvetica", 24))
        title_label.grid(row=0, column=1, padx=20)

        # Game Description
        description_text = (
            "Hanjie, also known as Nonograms or Griddlers, is a logic puzzle game. "
            "The goal is to reveal a hidden picture by painting the correct cells on a grid. "
            "Solve puzzles of varying difficulty and enjoy the challenge!"
        )
        description_label = tk.Label(self, text=description_text, font=("Helvetica", 14), wraplength=600)
        description_label.pack(pady=20)

        # Player Pseudonym Entry
        pseudo_label = tk.Label(self, text="Enter Your Pseudonym:", font=("Helvetica", 12))
        pseudo_label.pack(pady=5)

        self.pseudo_entry = tk.Entry(self, width=40)
        self.pseudo_entry.pack(pady=10)

        # Configure Game Button
        start_button = tk.Button(self, text="Configure the Game", command=self.show_config_window, width=20, height=2)
        start_button.pack(pady=10)

        # Exit Game Button
        exit_button = tk.Button(self, text="Exit Game", command=self.exit_game, width=20, height=2)
        exit_button.pack(pady=10)

        # Rankings Section
        last_results_label = tk.Label(self, text="Rankings", font=("Helvetica", 16))
        last_results_label.pack(pady=10)

        self.last_results_labels = []

        self.last_results = [
            {"date": "2023-01-01", "player": "Donald", "result": 650},
            {"date": "2023-01-02", "player": "Mickey", "result": 800},
            {"date": "2023-01-03", "player": "Felix", "result": 640},
            # ... To be replaced by results stored in a csv or json file?
        ]

        self.update_last_results()

    def show_config_window(self):
        config_window = GameConfigWindow(self)
        config_window.focus_force()
        config_window.wait_window()

    def start_game(self, difficulty, grid_size, theme):
        player_name = self.pseudo_entry.get()
        if not player_name:
            messagebox.showerror("Error", "Please enter your pseudonym before starting the game.")
            return

        mypath = "pictures"
        imgs = listdir(mypath)
        if theme == "Travel":
            img = "pictures/donald.png"
        elif theme == "Cartoon":
            img = "pictures/donald.png"
        else:
            img = join(mypath, rd.choice(imgs))

        nbwidth, nbheight = grid_size.split("x")
        grid = (int(nbwidth), int(nbheight))
        #hanjie.start_game(difficulty, grid, img)
        result = 1000
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        self.last_results.append({"date": date, "player": player_name, "result": result})
        self.update_last_results()

    def exit_game(self):
        self.destroy()

    def update_last_results(self):
        for label in self.last_results_labels:
            label.destroy()

        self.last_results_labels = []

        sorted_results = sorted(self.last_results, key=lambda res: res["result"], reverse=True)

        for i, result in enumerate(sorted_results[-10:]):
            result_label = tk.Label(
                self,
                text=f"{i + 1}. Player: {result['player']} \t Date: {result['date']} \t Result: {result['result']}"
            )
            result_label.pack(anchor="w", padx=20)
            self.last_results_labels.append(result_label)


class GameConfigWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Game Configuration")
        self.geometry("400x500")

        difficulty_label = tk.Label(self, text="Select Difficulty:", font=("Helvetica", 12))
        difficulty_label.pack(pady=5)

        difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_combobox = ttk.Combobox(self, values=difficulty_options)
        self.difficulty_combobox.set(difficulty_options[0])
        self.difficulty_combobox.pack(pady=10)

        # grid_size_label = tk.Label(self, text="Select Grid Size:", font=("Helvetica", 12))
        # grid_size_label.pack(pady=5)
        #
        # self.grid_size_entry = tk.Entry(self)
        # self.grid_size_entry.pack(pady=10)
        # self.grid_size_entry.insert(0, "10x10")
        # grid_select_button = tk.Button(self, text="Grid Selection", command=self.selectGrid, width=20, height=2)
        # grid_select_button.pack(pady=10)

        # Create a frame for grid-related options
        options_frame = tk.Frame(self, padx=10, pady=10)
        options_frame.pack(padx=10, pady=10)

        # Create a frame for grid selection
        grid_selection_frame = tk.Frame(options_frame, padx=10, pady=10, borderwidth=2, relief="groove")
        grid_selection_frame.grid(row=0, column=0, columnspan=4, pady=10)

        # Create labels, entry boxes, and buttons for height
        tk.Label(grid_selection_frame, text="Height:").grid(row=0, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(grid_selection_frame)
        self.height_entry.insert(0, 5)  # Set default value
        self.height_entry.grid(row=0, column=1, padx=5, pady=5)
        height_increment_button = tk.Button(grid_selection_frame, text="▲", command=lambda: self.update_height(1))
        height_increment_button.grid(row=0, column=2, padx=5, pady=5)
        height_decrement_button = tk.Button(grid_selection_frame, text="▼", command=lambda: self.update_height(-1))
        height_decrement_button.grid(row=0, column=3, padx=5, pady=5)

        # Create labels, entry boxes, and buttons for width
        tk.Label(grid_selection_frame, text="Width:").grid(row=1, column=0, padx=5, pady=5)
        self.width_entry = tk.Entry(grid_selection_frame)
        self.width_entry.insert(0, 5)  # Set default value
        self.width_entry.grid(row=1, column=1, padx=5, pady=5)
        width_increment_button = tk.Button(grid_selection_frame, text="▲", command=lambda: self.update_width(1))
        width_increment_button.grid(row=1, column=2, padx=5, pady=5)
        width_decrement_button = tk.Button(grid_selection_frame, text="▼", command=lambda: self.update_width(-1))
        width_decrement_button.grid(row=1, column=3, padx=5, pady=5)

        # Create a button to trigger the grid creation
        create_button = tk.Button(options_frame, text="Grid Creator", command=self.grid_creator)
        create_button.grid(row=1, column=0, columnspan=4, pady=10)

        # Create a frame to display the grid
        grid_frame = tk.Frame(self, padx=10, pady=10)
        grid_frame.pack(padx=10, pady=10)

        theme_label = tk.Label(self, text="Select Theme:", font=("Helvetica", 12))
        theme_label.pack(pady=5)

        theme_options = ["Random", "Cartoon", "Travel", "Animals"]
        self.theme_combobox = ttk.Combobox(self, values=theme_options)
        self.theme_combobox.set(theme_options[0])
        self.theme_combobox.pack(pady=10)

        launch_button = tk.Button(
            self, text="Launch Game", command=self.launch_game, width=20, height=2
        )
        launch_button.pack(pady=10)

        exit_config_button = tk.Button(
            self, text="Exit Configuration", command=self.exit_config, width=20, height=2
        )
        exit_config_button.pack(pady=10)

    def update_width(self, action):
        current_value = self.width_entry.get()
        if current_value.isdigit():
            new_value = int(current_value) + action
            if new_value > 0:
                self.width_entry.delete(0, tk.END)
                self.width_entry.insert(0, new_value)

    def update_height(self, action):
        current_value = self.height_entry.get()
        if current_value.isdigit():
            new_value = int(current_value) + action
            if new_value > 0:
                self.height_entry.delete(0, tk.END)
                self.height_entry.insert(0, new_value)

    def grid_creator(self):
        # Retrieve values from entry boxes
        gridSlection_window = gbs.GridBoardSelectionWindow(self)
        gridSlection_window.focus_force()
        gridSlection_window.wait_window()
        
        height = gridSlection_window.height
        width = gridSlection_window.width

        self.update_height(height - int(self.height_entry.get()))
        self.update_width(width - int(self.width_entry.get()))
        

    def launch_game(self):
        difficulty = self.difficulty_combobox.get()
        grid_size = (int(self.width_entry.get()),int(self.height_entry.get()))
        theme = self.theme_combobox.get()

        self.master.start_game(difficulty, grid_size, theme)
        self.destroy()

    def exit_config(self):
        self.destroy()


if __name__ == "__main__":
    hanjie_homepage = HanjieHomePage()
    hanjie_homepage.mainloop()