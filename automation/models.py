from typing import NamedTuple

from .constants import OpCode


class Instruction(NamedTuple):

    opcode: OpCode
    args: tuple
