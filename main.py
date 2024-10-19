from PIL import Image
from overlay.overlay import overlay_images

back = Image.open("tests/sh.png")
fore = Image.open("tests/nikita.png")

result_image = overlay_images(back, fore, relative_position=(0.2, 0.5))

if result_image:
    result_image.save("tests/result.png", format="PNG")