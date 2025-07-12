import numpy as np
import seam_carving
from PIL import Image, ImageOps, ImageFilter

from .rgb import find_unused_color, to_rgb, to_rgba
from .utils import change_ratio, crop_image

__all__ = [
    "add_gradient_outline",
    "apply_seam_carving",
    "add_noise",
]


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


def apply_seam_carving(img: Image, width_scale: float, height_scale: float) -> Image:

    mask = find_unused_color(img)

    rgb_img = to_rgb(img, mask)

    data = np.array(rgb_img)
    src_h, src_w, _ = data.shape
    target_h, target_w = int(src_h * height_scale), int(src_w * width_scale)

    transformed = seam_carving.resize(
        data, (target_w, target_h),
    )
    transformed_img = Image.fromarray(transformed, "RGB")
    transformed_img = to_rgba(transformed_img, mask)

    x_scale = transformed_img.size[0] / img.size[0]
    y_scale = transformed_img.size[1] / img.size[1]

    return change_ratio(transformed_img, 1/x_scale, 1/y_scale)


def add_noise(img: Image, x_scale: float, y_scale: float):
    width, height = img.size
    return img.resize(
        (int(width * x_scale), int(height * y_scale))
    ).resize((width, height))


def add_images(img_1: Image, img_2: Image) -> Image:
    img_1 = img_1.resize(img_2.size) if img_1.size != img_2.size else img_1
    img_2 = img_2.resize(img_1.size) if img_2.size != img_1.size else img_2

    width, height = img_1.size
    result = Image.new("RGB", (width, height))

    pix1 = img_1.load()
    pix2 = img_2.load()
    res_pix = result.load()

    # Обработка каждого пикселя
    for x in range(width):
        for y in range(height):
            r1, g1, b1 = pix1[x, y]
            r2, g2, b2 = pix2[x, y]

            res_pix[x, y] = min(r1, r2), min(g1, g2), min(b1, b2)

    return result

