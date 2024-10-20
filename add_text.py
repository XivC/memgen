from typing import Callable

import numpy as np
import seam_carving
from PIL import Image, ImageDraw, ImageFont


def _split_by_halves(text: str):
    words = text.split("|")
    return words[0], words[1]


def _add_text_to_img(
        img: Image,
        coords: tuple[int, int],
        text: str,
        font_size: int = 15,
        sub_processor: Callable[[Image], Image] | None = None,
        **text_kwargs,
):
    base_image = img.convert("RGBA")
    text_image = Image.new('RGBA', img.size, (255, 255, 255, 0))
    font = ImageFont.truetype("impact.ttf", font_size)

    draw = ImageDraw.Draw(text_image)
    _, _, text_width, text_height = draw.textbbox(xy=(0, 0), text=text, font=font)

    x, y = coords[0] - text_width / 2, coords[1] - text_height / 2,
    draw.text((x, y), text, font=font, **text_kwargs)

    if sub_processor:
        stock_size = text_image.size
        text_image = sub_processor(text_image)
        text_image = text_image.resize(stock_size)
    return Image.alpha_composite(base_image, text_image)

def add_text(
        img: Image,
        text: str,
        font_size: int = 15,
        sub_processor: Callable[[Image], Image] | None = None,
) -> Image:
    top, bottom = _split_by_halves(text)
    x_top = img.width / 2
    y_top = img.height * 0.1
    x_bottom = img.width / 2
    y_bottom = img.height * 0.9

    img = _add_text_to_img(img, (x_top, y_top), top, font_size=font_size, fill="white", sub_processor=sub_processor,
                           stroke_width=3, stroke_fill="black")
    img = _add_text_to_img(img, (x_bottom, y_bottom), bottom, font_size=font_size, fill="yellow",
                           sub_processor=sub_processor, stroke_width=3, stroke_fill="black")

    return img
