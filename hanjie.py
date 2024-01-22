import tkinter as tk
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk
from display import display
from checkLabel import checkLabel

adjusted_image = None
root = None

def loadImage():
    """
    Open a selection window to let user choose the image to binarise. 
    """
    global root

    file_path = filedialog.askopenfilename(title="Select a file", initialdir="pictures")
    if file_path:

        print("Selected file (path): ", file_path)
        grid = showBinarizedImage(file_path)

        labelsX, labelsY = checkLabel(grid)

        for i, row in enumerate(grid): print(i, row)
        display(grid, labelsX, labelsY, 1, 1)

    

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
    initial_image_height, initial_image_width = original_image.shape[:2]
    image_ratio = initial_image_width/initial_image_height

    max_grid_size = 25
    max_image_size = max(initial_image_height,initial_image_width)
    if max_image_size==initial_image_height :
        initial_image_size = (int(image_ratio*max_grid_size), max_grid_size)
    else :
        initial_image_size = (max_grid_size, int(max_grid_size/image_ratio))


    _, binarized_image = cv.threshold(original_image, 128, 255, cv.THRESH_BINARY) 

    window = tk.Toplevel()
    window.title("Binarized Image")

    tk_image = ImageTk.PhotoImage(Image.fromarray(cv.resize(binarized_image, initial_image_size)))

    image_label = tk.Label(window, image=tk_image, width=initial_image_size[0], height=initial_image_size[1])
    image_label.pack(side=tk.LEFT, padx=10, pady=10)

    # Cursors frame
    cursors_frame = tk.Frame(window)
    cursors_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Slider to adjust the image size
    size_label = tk.Label(cursors_frame, text="Image Size:")
    size_label.pack()
    size_scale = tk.Scale(cursors_frame, from_=5, to=25, orient=tk.HORIZONTAL, command=lambda x: update_image())
    size_scale.set(25)
    size_scale.pack()

    # Slider to adjust the binarization intensity
    intensity_label = tk.Label(cursors_frame, text="Binarization Intensity:")
    intensity_label.pack()
    intensity_scale = tk.Scale(cursors_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda x: update_image())
    intensity_scale.set(128)
    intensity_scale.pack()

    # Slider to adjust the binarization intensity
    erosion_label = tk.Label(cursors_frame, text="Erosion size:")
    erosion_label.pack()
    erosion_scale = tk.Scale(cursors_frame, from_=1, to=50, orient=tk.HORIZONTAL, command=lambda x: update_image())
    erosion_scale.set(1)
    erosion_scale.pack()

    # Slider to adjust the display size
    disp_size_label = tk.Label(cursors_frame, text="Display size:")
    disp_size_label.pack()
    disp_size_scale = tk.Scale(cursors_frame, from_=1, to=121, orient=tk.HORIZONTAL, command=lambda x: update_image())
    disp_size_scale.set(24)
    disp_size_scale.pack()

    # Callback function for updating the image based on slider values
    def update_image():

        global adjusted_image
        global adjusted_displayed_image
        new_size = size_scale.get()
        new_intensity = intensity_scale.get()
        new_erosion_size = erosion_scale.get()
        resize_display_factor = disp_size_scale.get()/4
        new_display_size = (int(initial_image_size[0]*resize_display_factor), int(initial_image_size[1]*resize_display_factor))

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (new_erosion_size, new_erosion_size),(-1,-1))
        eroded_image = cv.erode(binarized_image, kernel)

        resized_image_factor = new_size/max_grid_size
        resized_image = cv.resize(eroded_image, (int(resized_image_factor*initial_image_size[0]), int(resized_image_factor*initial_image_size[1])))

        # Adjust the binarization intensity
        _, adjusted_image = cv.threshold(resized_image, new_intensity, 255, cv.THRESH_BINARY)
        
        adjusted_displayed_image = cv.resize(adjusted_image, new_display_size) 

        tk_updated_image = ImageTk.PhotoImage(Image.fromarray(adjusted_displayed_image))
        image_label.config(image=tk_updated_image, width=new_display_size[0], height=new_display_size[1])
        image_label.image = tk_updated_image  
        

    close_button = tk.Button(cursors_frame, text="Close", command=window.destroy)
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
