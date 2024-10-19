from PIL import Image

from add_text import add_text
from image_transform import apply_seam_carving
from outline.outline import add_gradient_outline
from overlay.overlay import overlay_images
from remove_metadata import remove_background_metadata

background = Image.open("tests/Dust_II.jpg")
foreground = Image.open("tests/nikita.png")

background = remove_background_metadata(background)
foreground = remove_background_metadata(foreground)

foreground = add_gradient_outline(foreground)

result_image = overlay_images(background, foreground, relative_position=(0.1, 0.5))
result_image = apply_seam_carving(result_image, 0.8, 0.5)
result_image = add_text(
    result_image,
    "Иду 1:15 | в пизду эту игру",
    font_size=45,
    sub_processor=lambda img: add_gradient_outline(img, 10,)
)

result_image = result_image.resize(background.size)
result_image.show()