import tkinter as tk
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk

adjusted_image = None


def loadImage():
    """
    Open a selection window to let user choose the image to binarise. 
    """
    file_path = filedialog.askopenfilename(title="Select a file", initialdir="pictures")
    if file_path:
        print("Selected file (path): ", file_path)
        print(showBinarizedImage(file_path))

    

def convert_to_grid(image_array):
    """
    Convert the binrized image in a grid of 0 - 1 values.
    """
    # binary_image = (image_array == 255).all(axis=2).astype(int)
    binary_image = (image_array == 255).astype(int)

    grid = [['x' if pixel == 0 else 'o' for pixel in row] for row in binary_image]

    grid = [row for row in grid if 'x' in row]
    col_indices = [i for i, col in enumerate(zip(*grid)) if 'x' in col]
    grid = [list(row[idx] for idx in col_indices) for row in grid]

    return grid


def showBinarizedImage(image_path):
    original_image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    _, binarized_image = cv.threshold(original_image, 128, 255, cv.THRESH_BINARY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))  

    initial_display_size = (150, 150)
    window = tk.Toplevel()
    window.title("Binarized Image")

    tk_image = ImageTk.PhotoImage(Image.fromarray(cv.resize(binarized_image, initial_display_size)))


    image_label = tk.Label(window, image=tk_image, width=initial_display_size[0], height=initial_display_size[1])
    image_label.pack()

    # Slider to adjust the image size
    size_label = tk.Label(window, text="Image Size:")
    size_label.pack()
    size_scale = tk.Scale(window, from_=5, to=50, orient=tk.HORIZONTAL, command=lambda x: update_image())
    size_scale.set(initial_display_size[0])
    size_scale.pack()

    # Slider to adjust the binarization intensity
    intensity_label = tk.Label(window, text="Binarization Intensity:")
    intensity_label.pack()
    intensity_scale = tk.Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_image())
    intensity_scale.set(128)
    intensity_scale.pack()

    # Callback function for updating the image based on slider values
    def update_image():

        global adjusted_image
        new_size = size_scale.get()
        new_intensity = intensity_scale.get()
        resized_image = cv.resize(binarized_image, (new_size, new_size))

        # Adjust the binarization intensity
        _, adjusted_image = cv.threshold(resized_image, new_intensity, 255, cv.THRESH_BINARY)

        tk_updated_image = ImageTk.PhotoImage(Image.fromarray(adjusted_image))
        image_label.config(image=tk_updated_image, width=2* initial_display_size[0], height=2* initial_display_size[1])
        image_label.image = tk_updated_image  

    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.pack()
    window.after(100, update_image)  
    window.mainloop()


    final_grid = convert_to_grid(adjusted_image) # insert HERE the image
    return final_grid


if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Selection")

    open_button = tk.Button(root, text="Select a file", command=loadImage)
    open_button.pack(pady=20)

    root.mainloop()
