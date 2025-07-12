from enum import Enum


class OpCode(str, Enum):
    TEXT = "TEXT"
    SEAM_CARVING = "SC"
    OVERLAY = "OV"
    OUTLINE = "OUTLINE"
    NOISE = "NOISE"
    RATIO = "RATIO"
    REMOVE_BACKGROUND_METADATA = "REBM"
    TO_RGB = "RGB"
    TO_RGBA = "RGBA"
    CHANGE_RATIO = "CHR"
    CROP_IMAGE = "CROP"
    ROTATE_IMAGE = "ROTATE"
    DECL = "DECL"
    RET = "RET"
    PUSH = "PUSH"
    POP = "POP"
    SV = "SV"
    CALL = "CALL"


