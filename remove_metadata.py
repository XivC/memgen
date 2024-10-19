from PIL import Image


def remove_background_metadata(image: Image.Image) -> Image.Image:
    """
    Убирает альфа-канал (метаданные о вырезанном фоне) из PNG-изображения.

    :param image: Объект изображения (Pillow Image) в формате PNG.
    :return: Изображение без альфа-канала (Pillow Image).
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    cleaned_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    cleaned_image.paste(image, (0, 0), mask=image)

    return cleaned_image
