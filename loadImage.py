import tkinter as tk
from tkinter import filedialog

def loadImage() -> str:
    """
    Let the user choose a picture and return the filePath
    """
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a file", initialdir="pictures")

    return file_path
