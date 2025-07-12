import numpy as np
from PIL import Image


def find_unused_color(image: Image, default: tuple[int, int, int] = (255, 255, 255)) -> tuple[int, int, int]:

    img = image.convert('RGBA')
    data = np.array(img)

    if img.mode == 'RGBA':
        opaque_pixels = data[data[:, :, 3] > 0]
        unique_colors = {tuple(pixel[:3]) for pixel in opaque_pixels}
    else:
        unique_colors = {tuple(pixel) for pixel in data.reshape(-1, 3)}

    candidates = [
        (255, 254, 253),
        (254, 255, 253),
        (253, 254, 255),
        (0, 1, 2),
        (1, 0, 2),
        (2, 1, 0),
        (255, 0, 1),
        (0, 255, 1),
        (255, 255, 254),
        (255, 254, 255),
        (254, 255, 255)
    ]

    for color in candidates:
        if color not in unique_colors:
            return color

    for r in [0, 255]:
        for g in [0, 255]:
            for b in [0, 255]:
                if (r, g, b) not in unique_colors:
                    return (r, g, b)

    return default


def to_rgb(image: Image, fill_r: int, fill_g: int, fill_b: int) -> Image:
    if image.mode != 'RGBA':
        return image.convert('RGB')

    fill = (fill_r, fill_g, fill_b)
    data = np.array(image)
    rgb_data = data[:, :, :3].copy()
    alpha = data[:, :, 3]

    # Fill transparent pixels
    mask = (alpha == 0)
    for c in range(3):
        rgb_data[:, :, c][mask] = fill[c]

    return Image.fromarray(rgb_data, 'RGB')


def to_rgba(image: Image, remove_color_r: int | None = None, remove_color_g: int | None = None, remove_color_b: int | None = None) -> Image:
    img = image.convert('RGBA')

    remove_color = (remove_color_r, remove_color_g, remove_color_b)

    for i in remove_color:
        if i is None:
            return img

    data = np.array(img)
    r, g, b = remove_color

    # Create alpha channel (0 where color matches, 255 otherwise)
    mask = (data[:, :, 0] == r) & (data[:, :, 1] == g) & (data[:, :, 2] == b)
    data[:, :, 3] = np.where(mask, 0, 255)

    return Image.fromarray(data, 'RGBA')
