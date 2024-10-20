from PIL import Image

from add_text import add_text
from image_transform import apply_seam_carving
from outline.outline import add_gradient_outline
from overlay.overlay import overlay_images
from ratio import add_noise, change_ratio
from remove_metadata import remove_background_metadata

background = Image.open("tests/img_3.png")
foreground = Image.open("tests/gonchar.png")


foreground = remove_background_metadata(foreground)
foreground = foreground.resize((foreground.size[0] // 4, foreground.size[1] // 4))
foreground = foreground.resize((foreground.size[0] * 3, foreground.size[1] * 2))
foreground = add_gradient_outline(foreground)
foreground = add_noise(foreground, 0.9, 0.25)
foreground = change_ratio(foreground, 1.5, 0.9)

background = remove_background_metadata(background)
background = add_noise(background, 0.4, 1)
background = apply_seam_carving(background, 0.5, 0.5)

result_image = overlay_images(background, foreground, relative_position=(0.15, 0.5))
# result_image = apply_seam_carving(result_image, 0.8, 1.)
result_image = add_text(
    result_image,
    "ЗАКРОЙТЕ МЕНЯ В ЧЕТВЕРОМ | УЕБКИ",
    font_size=45,
    sub_processor=lambda img: add_gradient_outline(add_noise(img, 0.2, 0.3), 10,)
)

# result_image = apply_seam_carving(result_image, 0.9, 0.9)
result_image = result_image.resize(background.size)
result_image.show()