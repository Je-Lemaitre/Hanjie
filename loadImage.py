import tkinter as tk
from tkinter import filedialog

def loadImage():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a file", initialdir="pictures")

    return file_path
