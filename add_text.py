from typing import Callable

import numpy as np
import seam_carving
from PIL import Image, ImageDraw, ImageFont


def _split_by_halves(text: str):
    words = text.split("|")
    return words[0], words[1]


def get_text(
        text: str,
        font_size: int = 15,
        **text_kwargs,
):

    font = ImageFont.truetype("impact.ttf", font_size)
    _, _, text_width, text_height = font.getbbox(text=text)

    text_image = Image.new("RGBA", (int(text_width) + 20, int(text_height) + 20), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((10, 10), text, font=font, **text_kwargs)

    return text_image
