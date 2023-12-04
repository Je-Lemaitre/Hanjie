from PIL import Image, ImageFilter, ImageOps
import numpy as np

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

    return (left-20, top-20, right + 21, bottom + 21)

def binarise(img):
    image_path = img
    image = Image.open(image_path)

    image_data = image.convert('L').point(lambda x: 0 if x < 128 else 255)
    bbox = find_bounding_box(image_data)

    cropped_image = image.crop(bbox)
    new_width, new_height = cropped_image.size
    ratio = 10
    rescaled_image = cropped_image.resize((int(new_width/ratio), int(new_height/ratio)))

    rescaled_image = rescaled_image.convert('L')

    threshold_value = rescaled_image.getextrema()[0] / 2
    binary_image = ImageOps.autocontrast(rescaled_image, cutoff=threshold_value)

    edge_image = binary_image.filter(ImageFilter.FIND_EDGES)
    edge_image = edge_image.convert('1')

    width, height = edge_image.size
    bbox = 1, 1, width-1, height-1
    cropped_image = edge_image.crop(bbox)

    cropped_image.show()

    cropped_array = np.array(cropped_image)
