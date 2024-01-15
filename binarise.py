from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
from PIL import Image, ImageFilter, ImageOps, ImageTk
from PIL.Image import fromarray
import tkinter as tk
from tkinter import ttk

src = None
max_kernel_size = 20
max_image_size = 20
title_trackbar_kernel_size = 'Kernel size'
title_trackbar_image_size = 'Image size'
title_window = 'PRESS ANY KEY = PROCEED'

adjusted_image = None # tmp variable

def validate(state, userdata):
    print("Validation Button Clicked")

def convertToGrid(image_array):
    binary_image = (image_array == 255).all(axis=2).astype(int)

    grid = [['x' if pixel == 0 else 'o' for pixel in row] for row in binary_image]

    grid = [row for row in grid if 'x' in row]
    col_indices = [i for i, col in enumerate(zip(*grid)) if 'x' in col]
    grid = [list(row[idx] for idx in col_indices) for row in grid]

    if grid == []: return [['x']*image_array.shape[0]]*image_array.shape[1]
    return grid

def findBoundingBox(image):
    width, height = image.size
    left, top, right, bottom = width, height, 0, 0

    for x in range(1, width - 1):
        for y in range(1, height - 1):
            if image.getpixel((x, y)) == 0:  # Non-white pixel
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    return (left-1, top-1, right + 1, bottom + 1)

def processImage(src_erosion, image_size):

    # LOAD IMAGE, CROP, RESCALE
    ##############################
    src_to_PIL = fromarray(cv.cvtColor(src_erosion, cv.COLOR_BGR2RGB))
    src_data = src_to_PIL.convert('L').point(lambda x: 0 if x < 128 else 255)

    bbox = findBoundingBox(src_data)
    src_cropped = src_data.crop(bbox)

    new_width, new_height = src_cropped.size
    scale = 2.3
    ratio = max(new_width/image_size, new_height/image_size*scale)
    src_rescaled = src_cropped.resize((int(new_width/ratio), int(new_height/ratio)))

    src_rescaled = src_rescaled.convert('L').point(lambda x: 0 if x < 128 else 255)

    return(cv.cvtColor(np.array(src_rescaled), cv.COLOR_RGB2BGR))

def erosion(val):
    global eroded
    erosion_shape = cv.MORPH_RECT
    erosion_size = cv.getTrackbarPos(title_trackbar_kernel_size, title_window)
    image_size = cv.getTrackbarPos(title_trackbar_image_size, title_window) + 15

    element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                       (erosion_size, erosion_size))

    erosion_dst = cv.erode(src, element)

    erosion_processed = processImage(erosion_dst, image_size)
    eroded = erosion_processed

    cv.imshow(title_window, erosion_processed)

def binarise(image):
    global src
    global eroded
    src = cv.imread(cv.samples.findFile(image))
    height, width = src.shape[:2]
    scale_factor=max(200/height, 200/width)
    src = cv.resize(src, None, fx=scale_factor, fy=scale_factor, interpolation=cv.INTER_NEAREST)

    cv.namedWindow(title_window)

    cv.createTrackbar(title_trackbar_kernel_size, title_window, 2, max_kernel_size, erosion)
    cv.createTrackbar(title_trackbar_image_size, title_window, 10, max_image_size, erosion)

    cv.waitKey()

    cv.destroyAllWindows()

    finalGrid = convertToGrid(eroded)
    return finalGrid

def showBinarizedImage(image_path : str):
    """
    Display in a dialog window the binarized image selected.
    - The user need to custom binarisation factor and the size of the grid
    """
    original_image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    print(f" image path {image_path}, original image : {type(original_image)}")

    _, binarized_image = cv.threshold(original_image, 128, 255, cv.THRESH_BINARY)
    print(f"binarized image : {type(binarized_image)}")
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))  

    initial_display_size = (150, 150)
    # window = tk.Tk()
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
        print(f"adjusted image : {type(adjusted_image)}")
        tk_updated_image = ImageTk.PhotoImage(Image.fromarray(adjusted_image))
        image_label.config(image=tk_updated_image, width=2* initial_display_size[0], height=2* initial_display_size[1])
        image_label.image = tk_updated_image  
        

    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.pack()

    window.mainloop()
    window.after(100, update_image)  

    final_grid = convert_to_grid(adjusted_image) 
    print("after convert to grid")

    
    return final_grid


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

