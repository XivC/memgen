import numpy as np
from PIL import Image, ImageFilter, ImageOps


def add_gradient_outline(image: Image.Image, outline_width: int = 20, color: tuple = (255, 255, 0)) -> Image.Image:
    """
    Добавляет градиентную обводку к объекту на изображении (foreground),
    где цвет переходит от указанного (по умолчанию жёлтого) к прозрачному.

    :param image: Объект изображения (Pillow Image), которому нужно добавить градиентную обводку.
    :param outline_width: Ширина обводки.
    :param color: Цвет для обводки (по умолчанию жёлтый).
    :return: Изображение с градиентной обводкой (Pillow Image).
    """
    image = image.convert("RGBA")
    alpha = image.split()[3]

    outline_mask = ImageOps.expand(alpha, border=outline_width, fill=0)

    blurred_outline = outline_mask.filter(ImageFilter.GaussianBlur(radius=outline_width / 4))

    gradient_outline = Image.new('RGBA', blurred_outline.size)

    blurred_data = np.array(blurred_outline)
    max_alpha_value = np.max(blurred_data)

    for y in range(gradient_outline.height):
        for x in range(gradient_outline.width):
            alpha_value = blurred_data[y, x]
            if alpha_value > 0:
                new_alpha = int((alpha_value / max_alpha_value) ** 0.5 * 255)
                gradient_outline.putpixel((x, y), color + (new_alpha,))

    gradient_outline.paste(image, (outline_width, outline_width), mask=alpha)

    return gradient_outline
