from PIL import Image
from outline.outline import add_gradient_outline

image_path = "tests/nikita.png"
foreground_img = Image.open(image_path)

image_with_gradient_outline = add_gradient_outline(foreground_img)

image_with_gradient_outline.save("tests/out/res.png", format="PNG")