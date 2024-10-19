from PIL import Image
from outline.outline import add_gradient_outline
from overlay.overlay import overlay_images

back = Image.open("tests/Dust_II.jpg")
foreground = Image.open("tests/nikita.png")

foreground_outlined = add_gradient_outline(foreground)
result_image = overlay_images(back, foreground_outlined, relative_position=(0.2, 0.5))

if result_image:
    result_image.save("tests/out/res2.png", format="PNG")