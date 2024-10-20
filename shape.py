import random

import numpy as np
import seam_carving
from PIL import Image


def shape_channels(img: Image, seed: int) -> Image:
    random.seed(seed)
    new_img = Image.new("RGBA", img.size)

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            rgb = list(pixel[:3])
            random.shuffle(rgb)
            new_img.putpixel((x, y), tuple(rgb) + pixel[3:])

    return new_img