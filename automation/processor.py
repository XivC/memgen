from enum import Enum
from typing import Callable, Any

from PIL import Image

import add_text
from memgen.effects import add_gradient_outline, apply_seam_carving, add_noise
from memgen.utils import overlay_images, change_ratio


class ImageProcessor:
  
    def __init__(self, *base_images: Image):
        self.images: dict[int, Image] = {}

        for idx, img in enumerate(base_images, start=1):
            self.images[idx] = img

    def process(self, effect_tree: dict) -> Image:
        opcode = OpCode(effect_tree["op"])
        operation = OPERATION_BY_OPCODE[opcode]
        args = effect_tree.get("args", [])
        kwargs = effect_tree.get("kwargs", {})
        return operation(
            *[self._val(arg) for arg in args],
            **{
                key: self._val(value) for key, value in kwargs.items()
            }
        )

    def _val(self, value: Any) -> Any:
        if isinstance(value, str) and value.startswith("$"):
            image_id = int(value.removeprefix("$"))
            if image_id in self.images:
                return self.images[image_id]
            raise ValueError(f"No candidate for image id {image_id}")
        elif isinstance(value, dict):
            return self.process(value)

        return value
