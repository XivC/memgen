from PIL import Image


def overlay_images(background_path: str,
                   foreground_path: str,
                   output_path: str,
                   relative_position: tuple = (0.5, 0.5)
                   ):
    """
    Накладывает foreground изображение на background изображение с поддержкой альфа-канала
    и позицией по относительным координатам.

    :param background_path: Путь к фону.
    :param foreground_path: Путь к переднему плану.
    :param output_path: Путь для сохранения результата.
    :param relative_position: Относительная позиция (например (0.5, 0.5) для центра).
    """
    try:
        background = Image.open(background_path).convert("RGBA")
        foreground = Image.open(foreground_path).convert("RGBA")

        bg_width, bg_height = background.size
        fg_width, fg_height = foreground.size

        x = int(bg_width * relative_position[0] - fg_width / 2)
        y = int(bg_height * relative_position[1] - fg_height / 2)

        background.paste(foreground, (x, y), foreground)

        background.save(output_path, format="PNG")
        print(f"Изображение сохранено в {output_path}")
    except Exception as e:
        print(f"Ошибка: {e}")