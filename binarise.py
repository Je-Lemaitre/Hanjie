from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
from PIL import Image, ImageFilter, ImageOps
from PIL.Image import fromarray

src = None
max_kernel_size = 20
max_image_size = 20
title_trackbar_kernel_size = 'Kernel size'
title_trackbar_image_size = 'Image size'
title_window = 'Adjust parameters!'

def convertToGrid(image_array):
    binary_image = (image_array == 255).all(axis=2).astype(int)
    grid = [['x' if pixel == 0 else 'o' for pixel in row] for row in binary_image]
    col_indices = [i for i, col in enumerate(zip(*grid)) if 'x' in col]
    filtered_grid = [[row[idx] for idx in col_indices] for row in grid]
    return filtered_grid if filtered_grid else [['x']*image_array.shape[0]]*image_array.shape[1]

def findBoundingBox(image):
    width, height = image.size
    rows = range(1, height - 1)
    cols = range(1, width - 1)

    left = min((x for x in cols if any(image.getpixel((x, y)) == 0 for y in rows)), default=width)
    right = max((x for x in cols if any(image.getpixel((x, y)) == 0 for y in rows)), default=0)
    top = min((y for y in rows if any(image.getpixel((x, y)) == 0 for x in cols)), default=height)
    bottom = max((y for y in rows if any(image.getpixel((x, y)) == 0 for x in cols)), default=0)

    return (left - 1, top - 1, right + 1, bottom + 1)

def processImage(src_erosion, size=25):
    # LOAD IMAGE, CROP, RESCALE
    src_to_PIL = fromarray(cv.cvtColor(src_erosion, cv.COLOR_BGR2RGB))
    src_data = src_to_PIL.convert('L').point(lambda x: 0 if x < 128 else 255)

    bbox = findBoundingBox(src_data)
    src_cropped = src_data.crop(bbox)

    src_rescaled = src_cropped.resize((size, size))
    src_rescaled = src_rescaled.convert('L').point(lambda x: 0 if x < 128 else 255)
    return(cv.cvtColor(np.array(src_rescaled), cv.COLOR_RGB2BGR))


def erosion_kernel(val, erosion_size, resize_factor):
    erosion_size[0] = val
    update_image(erosion_size[0], resize_factor[0]/10)

def erosion_image(val, erosion_size, resize_factor):
    resize_factor[0] = max(val,1)
    update_image(erosion_size[0], resize_factor[0]/10)
    
def update_image(erosion_size, resize_factor):
    global eroded
    # Resize the image
    resized_image = cv.resize(src, None, fx=resize_factor, fy=resize_factor, interpolation=cv.INTER_NEAREST)

    # Create a structuring element for erosion
    erosion_shape = cv.MORPH_RECT
    element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),(-1,-1))

    # Apply erosion
    eroded_image = cv.erode(resized_image, element)
    eroded = eroded_image
    # Display the image
    cv.imshow(title_window, eroded_image)

def binarise(image):
    global src
    global init_dimensions
    src = cv.imread(cv.samples.findFile(image))
    erosion_size = [0]
    resize_factor = [10]
    init_dimensions = np.array(src.shape[:2])

    cv.namedWindow(title_window,flags=cv.WINDOW_FULLSCREEN)

    cv.createTrackbar(title_trackbar_kernel_size, title_window, 0, max_kernel_size, lambda val: erosion_kernel(val, erosion_size, resize_factor))
    cv.createTrackbar(title_trackbar_image_size, title_window, 0, max_image_size, lambda val: erosion_image(val, erosion_size, resize_factor))

    update_image(erosion_size[0], resize_factor[0]/10)
    cv.waitKey(0)
    cv.destroyAllWindows()

    eroded_processed = processImage(eroded,20)

    return convertToGrid(eroded_processed)