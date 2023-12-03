import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk

class HanjieHomePage:
    def __init__(self, master):
        self.master = master
        master.title("Hanjie Game")

        # Configure row and column weights for resizing
        for i in range(3):  # Three rows
            master.rowconfigure(i, weight=1)
        for i in range(4):  # Four columns
            master.columnconfigure(i, weight=1)

        # Title label
        title_font = ('Meiryo', 20, 'bold')
        title_label = tk.Label(master, text="Hanjie Game", font=title_font, fg="orange")
        title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nw')

        # Login button, Avatar, and Settings button
        login_button = tk.Button(master, text="Login")
        login_button.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # Avatar as a round box
        avatar_image = Image.open("pictures/scooby doo.jpg")  # Replace with the path to your avatar image
        avatar_image = avatar_image.resize((50, 50), Image.ANTIALIAS)
        avatar_image = ImageTk.PhotoImage(avatar_image)

        avatar_label = tk.Label(master, image=avatar_image, borderwidth=2, relief="solid")
        avatar_label.image = avatar_image  # To prevent garbage collection
        avatar_label.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # Settings button
        settings_button = ttk.Button(master, text="Settings", command=self.open_settings)
        settings_button.grid(row=0, column=3, padx=10, pady=10, sticky='e')

        # Button to start a new game
        new_game_button = tk.Button(master, text="Start New Game", command=self.start_new_game, )
        new_game_button.grid(row=1, column=0, columnspan=4, pady=20, sticky="nsew")

        # Box with a list of previous games, pseudos, scores, and dates
        games_box = tk.Listbox(master, selectmode=tk.SINGLE, height=10, width=40)
        games_box.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
        master.columnconfigure(0, weight=1)  # Adjust column weight for the results box

        # Add sample previous games and scores (you can replace this with your data)
        sample_games = [("Player1", 100, "2023-01-01"), ("Player2", 150, "2023-02-15"), ("Player3", 120, "2023-03-10")]
        sample_games.sort(key=lambda x: x[1], reverse=True)  # Sort by score in descending order

        for pseudo, score, date in sample_games:
            games_box.insert(tk.END, f"Pseudo: {pseudo} | Score: {score} | Date: {date}")

    def start_new_game(self):
        # Add logic to start a new game here
        hanjie_game_window = tk.Toplevel(self.master)
        app = HanjieGameWindow(hanjie_game_window)
        print("Starting a new game...")

    def open_settings(self):
        # Add logic to open settings here
        print("Opening settings...")

class HanjieGameWindow:
    def __init__(self, master):
        self.master = master
        master.title("Hanjie Game")

        # Configure row and column weights for resizing
        for i in range(4):  # Four rows
            master.rowconfigure(i, weight=1)
        for i in range(4):  # Four columns
            master.columnconfigure(i, weight=1)

        # Title label with Japanese-style font
        title_font = ('Meiryo', 20, 'bold')
        title_label = tk.Label(master, text="Hanjie Game", font=title_font, fg="orange")
        title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='nw')  # Use 'nw' for sticky

        # Avatar as a round box
        avatar_image = Image.open("pictures/scooby doo.jpg")  # Replace with the path to your avatar image
        avatar_image = avatar_image.resize((50, 50), Image.ANTIALIAS)
        avatar_image = ImageTk.PhotoImage(avatar_image)

        avatar_label = tk.Label(master, image=avatar_image, borderwidth=2, relief="solid")
        avatar_label.image = avatar_image  # To prevent garbage collection
        avatar_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')

        # Settings button with a gear icon
        settings_button = ttk.Button(master, text="Settings", command=self.open_settings)
        settings_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        # Combo box for theme selection
        themes = ["Theme 1", "Theme 2", "Theme 3"]  # Replace with your themes
        theme_label = tk.Label(master, text="Theme:")
        theme_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        theme_combobox = ttk.Combobox(master, values=themes)
        theme_combobox.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Combo box for difficulty selection
        difficulties = ["Easy", "Medium", "Hard"]  # Replace with your difficulties
        difficulty_label = tk.Label(master, text="Difficulty:")
        difficulty_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        difficulty_combobox = ttk.Combobox(master, values=difficulties)
        difficulty_combobox.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Button to launch Hanjie game (filling width)
        launch_button = tk.Button(master, text="Launch Hanjie", command=self.launch_hanjie)
        launch_button.grid(row=3, column=0, columnspan=4, pady=20, sticky='nsew')

        # Button to return to the home window
        return_button = tk.Button(master, text="Return to Home", command=self.return_to_home)
        return_button.grid(row=3, column=0, padx=10, pady=10, sticky='sw')

    def open_settings(self):
        # Add logic to open settings here
        print("Opening settings...")

    def launch_hanjie(self):
        # Add logic to launch Hanjie game here
        print("Launching Hanjie game...")

    def return_to_home(self):
        # Add logic to return to the home window here
        print("Returning to home...")

if __name__ == "__main__":
    root = tk.Tk()
    app = HanjieHomePage(root)
    root.mainloop()
    # root2 = tk.Tk()
    # app2 = HanjieGameWindow(root2)
    # root2.mainloop()
