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


def to_rgb(image: Image, fill: tuple[int, int, int]) -> Image:
    """
    Converts RGBA image to RGB, filling transparent pixels with specified color.

    Args:
        image: PIL Image in RGBA mode
        fill: Tuple of (R, G, B) for filling transparent areas

    Returns:
        PIL Image in RGB mode
    """
    if image.mode != 'RGBA':
        return image.convert('RGB')

    data = np.array(image)
    rgb_data = data[:, :, :3].copy()
    alpha = data[:, :, 3]

    # Fill transparent pixels
    mask = (alpha == 0)
    for c in range(3):
        rgb_data[:, :, c][mask] = fill[c]

    return Image.fromarray(rgb_data, 'RGB')


def to_rgba(image: Image, remove_color: tuple[int, int, int] | None = None) -> Image:
    """
    Converts RGB image to RGBA, optionally making a specific color transparent.

    Args:
        image: PIL Image in RGB mode
        remove_color: Tuple of (R, G, B) to make transparent. If None, returns opaque RGBA.

    Returns:
        PIL Image in RGBA mode
    """
    img = image.convert('RGBA')

    if remove_color is None:
        return img

    data = np.array(img)
    r, g, b = remove_color

    # Create alpha channel (0 where color matches, 255 otherwise)
    mask = (data[:, :, 0] == r) & (data[:, :, 1] == g) & (data[:, :, 2] == b)
    data[:, :, 3] = np.where(mask, 0, 255)

    return Image.fromarray(data, 'RGBA')
