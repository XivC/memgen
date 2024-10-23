from enum import Enum
from typing import Callable, Any

from PIL import Image

import add_text
from image_transform import apply_seam_carving
from outline.outline import add_gradient_outline
from overlay.overlay import overlay_images
from ratio import add_noise, change_ratio


class OpType(str, Enum):
    GENERATING = "GENERATING"
    UNARY = "UNARY"
    BINARY = "BINARY"


class OpCode(str, Enum):
    TEXT = "text"
    SEAM_CARVING = "seam_carving"
    OVERLAY = "overlay"
    OUTLINE = "outline"
    NOICE = "noise"
    RATIO = "ratio"


OPERATION_BY_OPCODE: dict[OpCode, Callable] = {
    OpCode.TEXT: add_text,
    OpCode.SEAM_CARVING: apply_seam_carving,
    OpCode.OVERLAY: overlay_images,
    OpCode.OUTLINE: add_gradient_outline,
    OpCode.NOICE: add_noise,
    OpCode.RATIO: change_ratio,
}

OPCODE_TYPE: dict[OpCode, OpType] = {
    OpCode.TEXT: OpType.GENERATING,
    OpCode.SEAM_CARVING: OpType.UNARY,
    OpCode.OVERLAY: OpType.BINARY,
    OpCode.OUTLINE: OpType.UNARY,
    OpCode.NOICE: OpType.UNARY,
    OpCode.RATIO: OpType.UNARY,
}


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
