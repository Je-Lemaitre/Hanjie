import tkinter as tk
from tkinter import filedialog

def loadImage() -> str:
    """    
    Return the file Path
    """
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a file", initialdir="pictures")

    return file_path
