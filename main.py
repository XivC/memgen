from overlay.overlay import overlay_images

back = "tests/sh.png"
fore = "tests/nikita.png"

out = "tests/out/result.png"
overlay_images(back, fore, out)