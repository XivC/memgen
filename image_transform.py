import numpy as np
import seam_carving
from PIL import Image


def _color_dist(col1: tuple[int, int, int], col2: tuple[int, int, int]):
    sm = 0
    for x1, x2 in zip(col1, col2):
        sm += (x1 - x2)**2

    return sm ** 0.5


def _to_rgba(img: Image) -> Image:
    void_color = (255, 255, 255, 0)
    data = img.getdata()
    new_data = []
    for item in data:
        if _color_dist(item[:2], (0, 0, 0)) < 5:
            new_data.append(void_color)
        else:
            new_data.append(item)

    # Create a new image with replaced black pixels
    image_with_void = Image.new("RGBA", img.size)
    image_with_void.putdata(new_data)

    return image_with_void


def apply_seam_carving(img: Image, width_scale: float, height_scale: float) -> Image:

    rgb_img = img.convert("RGB")
    data = np.array(rgb_img)
    src_h, src_w, _ = data.shape
    target_h, target_w = int(src_h * height_scale), int(src_w * width_scale)

    transformed = seam_carving.resize(
        data, (target_w, target_h),
    )
    transformed_img = Image.fromarray(transformed)
    return _to_rgba(transformed_img)

