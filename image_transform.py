import numpy as np
import seam_carving
from PIL import Image


def apply_seam_carving(img: Image, width_scale: float, height_scale: float) -> Image:

    data = np.array(img)
    src_h, src_w, _ = data.shape
    target_h, target_w = int(src_h * height_scale), int(src_w * width_scale)

    transformed = seam_carving.resize(
        data, (target_w, target_h),
    )
    return Image.fromarray(transformed)

