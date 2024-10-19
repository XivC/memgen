from PIL import Image

from add_text import add_text
from image_transform import apply_seam_carving

test = Image.open("tests/img.png")

test = apply_seam_carving(test, 0.9, 0.5)
test = add_text(test, "Умоляю тебя выеби меня сковородкой", 30)

test.show()