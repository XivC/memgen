from PIL import Image


def overlay_images(background: Image.Image, foreground: Image.Image,
                   relative_position: tuple = (0.5, 0.5)) -> Image.Image:
    """
    Накладывает foreground изображение на background изображение с поддержкой альфа-канала
    и позицией по относительным координатам.

    :param background: Объект background изображения (Pillow Image).
    :param foreground: Объект foreground изображения (Pillow Image).
    :param relative_position: Относительная позиция (например (0.5, 0.5) для центра).
    :return: Изображение после наложения (Pillow Image).
    """
    try:
        background = background.convert("RGBA")
        foreground = foreground.convert("RGBA")

        bg_width, bg_height = background.size
        fg_width, fg_height = foreground.size

        x = int(bg_width * relative_position[0] - fg_width / 2)
        y = int(bg_height * relative_position[1] - fg_height / 2)

        background.paste(foreground, (x, y), foreground)

        return background
    except Exception as e:
        print(f"Ошибка: {e}")
        return None