import numpy as np
from PIL import Image, ImageFont, ImageDraw

__all__ = [
    "overlay_images",
    "get_text",
    "change_ratio",
]

from PIL.Image import Transpose


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

    font = ImageFont.truetype("impact.ttf", font_size)
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
        return resized.transpose(Transpose.ROTATE_180)
    elif x_scale < 0:
        return resized.transpose(Transpose.FLIP_LEFT_RIGHT)
    elif y_scale < 0:
        return resized.transpose(Transpose.FLIP_TOP_BOTTOM)

    return resized


def crop_image(image: Image) -> Image:
    """
    Crop the image to remove borders with fully transparent pixels.

    Args:
        image: PIL Image in RGBA mode

    Returns:
        Cropped PIL Image with transparent borders removed
    """
    if image.mode != 'RGBA':
        return image

    # Convert to numpy array
    data = np.array(image)
    alpha = data[:, :, 3]

    # Find rows and columns that contain non-transparent pixels
    rows_with_content = np.where(alpha.any(axis=1))[0]
    cols_with_content = np.where(alpha.any(axis=0))[0]

    if len(rows_with_content) == 0 or len(cols_with_content) == 0:
        return Image.new('RGBA', (0, 0))  # Return empty image if fully transparent

    # Determine crop boundaries
    top = rows_with_content[0]
    bottom = rows_with_content[-1]
    left = cols_with_content[0]
    right = cols_with_content[-1]

    # Crop the image
    return image.crop((left, top, right + 1, bottom + 1))


def rotate_image(img: Image, angle: float) -> Image:

    # Rotate while expanding the canvas to fit the rotated image
    rotated = img.rotate(
        angle,
        expand=True,  # Ensures the whole image fits without cropping
        resample=Image.BICUBIC,  # High-quality resampling
        fillcolor=None if img.mode == 'RGBA' else (255, 255, 255)  # Transparent for RGBA
    )

    return rotated