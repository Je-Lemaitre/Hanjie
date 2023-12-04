from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
from PIL import Image, ImageFilter, ImageOps
from PIL.Image import fromarray

src = None
max_kernel_size = 20
max_image_size = 21
title_trackbar_kernel_size = 'Kernel size'
title_trackbar_image_size = 'Image size'
title_window = 'Adjust parameters!'

def convert_to_grid(image_array):
    binary_image = (image_array == 255).all(axis=2).astype(int)
    grid = [['x' if pixel == 0 else 'o' for pixel in row] for row in binary_image]

    grid = [row for row in grid if 'x' in row]
    col_indices = [i for i, col in enumerate(zip(*grid)) if 'x' in col]
    grid = [list(row[idx] for idx in col_indices) for row in grid]

    return grid

def find_bounding_box(image):
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

    bbox = find_bounding_box(src_data)
    src_cropped = src_data.crop(bbox)

    new_width, new_height = src_cropped.size
    scale = 1920/1080
    ratio = max(new_width/image_size*scale, new_height/image_size)
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

    final_grid = convert_to_grid(eroded)
    return final_grid
