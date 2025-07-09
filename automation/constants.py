from enum import Enum
from typing import Callable

import add_text
from memgen.effects import add_gradient_outline, apply_seam_carving, add_noise
from memgen.utils import overlay_images, change_ratio


class OpType(str, Enum):
    GENERATING = "GENERATING"
    UNARY = "UNARY"
    BINARY = "BINARY"
    CONTROL = "CONTROL"


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
