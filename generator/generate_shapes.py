from PIL import Image
from tqdm import tqdm
from typing import Tuple
import fisheye
import numpy as np
import math
import os
from matplotlib import pyplot as plt


# get a square submap of size size
def square(map, x, y, size):
    return map[
        x - int(size / 2) : x + int(size / 2), y - int(size / 2) : y + int(size / 2)
    ]


# threshold the noise map
def threshold_noise(map, threshold):
    return np.where(map < threshold, 0, 1)


def pad_colorized_array(array, padding):
    pad_width = [(padding, padding), (padding, padding), (0, 0)]
    constant_values = [(255, 255), (255, 255), (255, 255)]
    return np.pad(array, pad_width, mode="constant", constant_values=constant_values)


def pad_array(array, padding):
    pad_width = [(padding, padding), (padding, padding)]
    return np.pad(array, pad_width, mode="constant", constant_values=0)


def generate_shapes(
    symbol_size: int, image_directory: str, words: Tuple[str], map, points
):
    if not os.path.exists(image_directory):
        os.mkdir(image_directory)

    for file in os.listdir(image_directory):
        os.remove(os.path.join(image_directory, file))

    for i, point in tqdm(enumerate(points)):
        submap = square(map, int(point[0]), int(point[1]), symbol_size)

        if len(submap.shape) == 3:  # colorized, likely RGB
            submap = pad_colorized_array(submap, symbol_size)
        else:
            submap = pad_array(submap, symbol_size)

        F = fisheye.fisheye(R=(symbol_size / 2) * math.sqrt(2), d=5)
        F.set_focus([symbol_size * 1.5, symbol_size * 1.5])
        F.set_mode("Sarkar")

        array = fisheye.apply_to_image(submap, F)
        array = np.squeeze(array)  # Remove the extra dimension

        array = np.clip(array, 0, 1)
        array = (array * 255).astype(np.uint8)  # Scale and convert to uint8

        im = Image.fromarray(array)
        im.save(
            "{}/{}-({},{}).png".format(
                image_directory, words[i], int(point[0]), int(point[1])
            )
        )

    return
