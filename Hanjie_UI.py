import customtkinter as ctk
from PIL import Image, ImageTk
from datetime import datetime

ctk.set_default_color_theme("dark-blue")


class HanjieHomePage(ctk.CTk):
    """
    Implement the Home Page of the game Hanjie in Custom Tkinter
    """
    def __init__(self):
        super().__init__()
        self.title("Hanjie - Puzzle Game")
        self.geometry("800x600")
        self.configure()

        # Header with Title and Image

        # Load and resize the game image
        game_image = ctk.CTkImage(Image.open("hanjie_image.png") , size=(50,50))
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(pady=20)

        image_label = ctk.CTkLabel(header_frame, image=game_image)
        image_label.grid(row=0, column=0, padx=10)

        title_label = ctk.CTkLabel(header_frame, text="Welcome to Hanjie - Puzzle Game", font=("Helvetica", 24))
        title_label.grid(row=0, column=1, padx=20)

        # Game Description
        description_text = (
            "Hanjie, also known as Nonograms or Griddlers, is a logic puzzle game. "
            "The goal is to reveal a hidden picture by painting the correct cells on a grid. "
            "Solve puzzles of varying difficulty and enjoy the challenge!"
        )
        description_label = ctk.CTkLabel(self, text=description_text, font=("Helvetica", 14), wraplength=600)
        description_label.pack(pady=20)

        # Player Pseudonym Entry
        pseudo_label = ctk.CTkLabel(self, text="Enter Your Pseudonym:", font=("Helvetica", 12))
        pseudo_label.pack(pady=5)

        self.pseudo_entry = ctk.CTkEntry(self, width=200)
        self.pseudo_entry.pack(pady=10)

        # Configure Game Button
        start_button = ctk.CTkButton(self, text="Configure the Game", command=self.show_config_window, width=20, height=2)
        start_button.pack(pady=10)

        # Exit Game Button
        exit_button = ctk.CTkButton(self, text="Exit Game", command=self.exit_game, width=20, height=2)
        exit_button.pack(pady=10)

        # Rankings Section
        last_results_label = ctk.CTkLabel(self, text="Rankings", font=("Helvetica", 16))
        last_results_label.pack(pady=10)

        self.last_results_labels = []  # Store references to the labels displaying results

        # Store the last results in this list
        self.last_results = [
            {"date": "2023-01-01", "player": "Donald", "result": 650},
            {"date": "2023-01-02", "player": "Mickey", "result": 800},
            {"date": "2023-01-03", "player": "Felix", "result": 640},
            # ... To be replaced by results stored in a csv or json file ?
        ]

        # Display initial results on the home page
        self.update_last_results()

    def show_config_window(self):
        config_window = GameConfigWindow(self)
        config_window.focus_force()
        config_window.wait_window()

    def start_game(self, difficulty, grid_size, theme):
        # Get the player's pseudonym
        player_name = self.pseudo_entry.get()
        if not player_name:
            textbox = ctk.CTkTextbox(self)
            textbox.configure(state="disabled")
            textbox.insert("0.0","Error: Please enter your pseudonym before starting the game.")
            print("Error: Please enter your pseudonym before starting the game.")
            return

        # Add the code to launch the game with selected difficulty, grid size, and theme
        # Here is a result, for example
        result = 1000  # Replace with actual game result
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Store the result
        self.last_results.append({"date": date, "player": player_name, "result": result})

        # Update the last results labels
        self.update_last_results()

    def exit_game(self):
        # The data may be saved before closing the window.
        self.destroy()  # Close the main window

    def update_last_results(self):
        # Display the last 10 results on the home page
        for label in self.last_results_labels:
            label.destroy()

        self.last_results_labels = []

        sorted_results = sorted(self.last_results, key=lambda res:res["result"], reverse=True)

        for i, result in enumerate(sorted_results[-10:]):
            result_label = ctk.CTkLabel(
                self, text=f"{i + 1}. Player: {result['player']} \t Date: {result['date']} \t Result: {result['result']}"
            )
            result_label.pack(anchor="w", padx=20)
            self.last_results_labels.append(result_label)


class GameConfigWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Game Configuration")
        self.geometry("400x300")
        self.configure()

        # Difficulty Selection
        difficulty_label = ctk.CTkLabel(self, text="Select Difficulty:", font=("Helvetica", 12))
        difficulty_label.pack(pady=5)

        difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_combobox = ctk.CTkComboBox(self, values=difficulty_options)
        self.difficulty_combobox.set(difficulty_options[0])  # Default: Easy
        self.difficulty_combobox.pack(pady=10)

        # Grid Size Selection
        grid_size_label = ctk.CTkLabel(self, text="Select Grid Size:", font=("Helvetica", 12))
        grid_size_label.pack(pady=5)

        self.grid_size_entry = ctk.CTkEntry(self)
        self.grid_size_entry.pack(pady=10)
        self.grid_size_entry.insert(0,"10x10")

        # Theme Selection
        theme_label = ctk.CTkLabel(self, text="Select Theme:", font=("Helvetica", 12))
        theme_label.pack(pady=5)

        theme_options = ["Random","Cartoon", "Travel", "Animals"]  # Replace with your theme options
        self.theme_combobox = ctk.CTkComboBox(self, values=theme_options)
        self.theme_combobox.set(theme_options[0])  # Default: Random
        self.theme_combobox.pack(pady=10)

        # Launch Game Button
        launch_button = ctk.CTkButton(
            self, text="Launch Game", command=self.launch_game, width=20, height=2
        )
        launch_button.pack(pady=10)

    def launch_game(self):
        # Get selected difficulty, grid size, and theme
        difficulty = self.difficulty_combobox.get()
        grid_size = self.grid_size_entry.get()
        theme = self.theme_combobox.get()

        # Call the start_game method in the main window with selected options
        self.master.start_game(difficulty, grid_size, theme)
        self.destroy()


if __name__ == "__main__":
    hanjie_homepage = HanjieHomePage()
    hanjie_homepage.mainloop()
