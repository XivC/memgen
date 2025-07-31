import os
import platform

import numpy as np
from PIL import Image, ImageFont, ImageDraw

__all__ = [
    "overlay_images",
    "get_text",
    "change_ratio",
    "rotate_image",
    "crop_image"
]


FONT_CANDIDATES = {
    "Windows": [
        r"C:\Windows\Fonts\impact.ttf",
        r"C:\Windows\Fonts\arialbd.ttf"
    ],
    "Darwin": [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    ],
    "Linux": [
        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
}

def get_font_path():
    system = platform.system()
    candidates = FONT_CANDIDATES.get(system, [])

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


def overlay_images(
        background: Image.Image,
        foreground: Image.Image,
        relative_x: float = 0.5,
        relative_y: float = 0.5,
) -> Image.Image:

    background = background.convert("RGBA")
    foreground = foreground.convert("RGBA")

    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size

    x = int(bg_width * relative_x - fg_width / 2)
    y = int(bg_height * relative_y - fg_height / 2)

    background.paste(foreground, (x, y), foreground)

    return background


def get_text(
        text: str,
        font_size: int = 15,
        fill: str = "white",
        stroke_width: int = None,
):

    font_path = get_font_path()
    if not font_path:
        font = ImageFont.load_default(font_size)
    else:
        font = ImageFont.truetype(font_path, font_size)

    _, _, text_width, text_height = font.getbbox(text=text)

    if not stroke_width:
        stroke_width = font_size // 15

    text_image = Image.new("RGBA", (int(text_width) + 20, int(text_height) + 20), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((10, 10), text, font=font, fill=fill, stroke_fill="black", stroke_width=stroke_width)

    return text_image


def change_ratio(img: Image, x_scale: float, y_scale: float) -> Image:
    width, height = img.size

    new_width = int(abs(x_scale) * width)
    new_height = int(abs(y_scale) * height)

    resized = img.resize((new_width, new_height))

    if x_scale < 0 and y_scale < 0:
        return resized.transpose(Image.Transpose.ROTATE_180)
    elif x_scale < 0:
        return resized.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif y_scale < 0:
        return resized.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    return resized


def crop_image(image: Image) -> Image:
    if image.mode != 'RGBA':
        return image

    data = np.array(image)
    alpha = data[:, :, 3]
    rows_with_content = np.where(alpha.any(axis=1))[0]
    cols_with_content = np.where(alpha.any(axis=0))[0]

    if len(rows_with_content) == 0 or len(cols_with_content) == 0:
        return Image.new('RGBA', (0, 0))

    top = rows_with_content[0]
    bottom = rows_with_content[-1]
    left = cols_with_content[0]
    right = cols_with_content[-1]

    return image.crop((left, top, right + 1, bottom + 1))


def rotate_image(img: Image, angle: float) -> Image:

    rotated = img.rotate(
        angle,
        expand=True,
        resample=Image.BICUBIC,
        fillcolor=None if img.mode == 'RGBA' else (255, 255, 255)
    )

    return rotated