from PIL import Image


def add_noise(img: Image, x_scale: float, y_scale: float):
    width, height = img.size
    return img.resize(
        (int(width * x_scale), int(height * y_scale))
    ).resize((width, height))


def change_ratio(img: Image, x_scale: float, y_scale: float):
    width, height = img.size
    return img.resize(
        (int(width * x_scale), int(height * y_scale))
    )