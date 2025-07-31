from typing import Callable

from PIL import Image

from src.libimgen.automation.constants import OpCode
from src.libimgen.automation.models import Instruction
from src.libimgen import core


class Machine:

    def __init__(self, program: list[Instruction], initial_variables: dict[str, Image] | None = None):
        self.program = program
        self.variables = initial_variables if initial_variables is not None else {}
        self.known_functions = self.find_known_functions() | self.get_default_known_functions()
        self.instruction_ptr = self.find_program_start()
        self.call_stack = []
        self.img_stack = []

    def find_program_start(self):
        if "main" in self.known_functions:
            return self.known_functions["main"][0]

        return 0

    def find_known_functions(self) -> dict[str, int]:

        result = {}
        for iptr, instruction in enumerate(self.program):
            if instruction.opcode == OpCode.DECL:
                if len(instruction.args) < 1:
                    raise ValueError(f"Invalid declaration in {iptr}: Unnamed functions not supported")

                func_name = instruction.args[0]
                if len(instruction.args) > 1:
                    img_count = instruction.args[1]
                else:
                    img_count = 0

                result[func_name] = (iptr, img_count)

        return result

    def run(self) -> Image:

        while True:
            instruction = self.fetch()
            if not instruction:
                return self.safe_pop()

            self.execute(instruction)
            self.instruction_ptr += 1

    def fetch(self) -> Instruction | None:
        try:
            return self.program[self.instruction_ptr]
        except IndexError:
            return None

    def execute(self, instruction: Instruction) -> None:
        opcode, args = instruction

        if opcode in self.known_functions:
            instr, img_count = self.known_functions[opcode]
            if isinstance(instr, int):
                self.call(instr)
                return
            else:
                img_args = [self.safe_pop() for _ in range(img_count)]
                if len(args) > 0 and args[0] == "~":
                    args = args[1:]
                    img_args = img_args[::-1]

                result = instr(*img_args, *args)
                if result:
                    self.img_stack.append(result)

    def call(self, to: str) -> None:

        target_addr, _ = self.known_functions.get(to, (None, None))
        if target_addr is None:
            raise ValueError(f"Unknown declaration {to} in {self.instruction_ptr}")

        self.call_stack.append(self.instruction_ptr)
        self.instruction_ptr = target_addr

    def push(self, var_name: str) -> None:
        img = self.get_var(var_name)
        self.img_stack.append(img)

    def ret(self) -> None:
        try:
            new_iptr = self.call_stack.pop()
        except IndexError:
            raise ValueError(f"Call stack is empty: {self.instruction_ptr}")

        self.instruction_ptr = new_iptr

    def save(self, var_name: str) -> None:
        try:
            top = self.img_stack[-1]
        except IndexError:
            raise ValueError(f"Stack is empty: {self.instruction_ptr}")

        self.variables[var_name] = top

    def get_default_known_functions(self) -> dict[str, tuple[Callable, int]]:
        return {
            OpCode.TEXT: (core.get_text, 0),
            OpCode.SEAM_CARVING: (core.apply_seam_carving, 1),
            OpCode.OVERLAY: (core.overlay_images, 2),
            OpCode.OUTLINE: (core.add_gradient_outline, 1),
            OpCode.NOISE: (core.add_noise, 1),
            OpCode.RATIO: (core.change_ratio, 1),
            OpCode.REMOVE_BACKGROUND_METADATA: (core.remove_background_metadata, 1),
            OpCode.TO_RGB: (core.to_rgb, 1),
            OpCode.TO_RGBA: (core.to_rgba, 1),
            OpCode.CHANGE_RATIO: (core.change_ratio, 1),
            OpCode.CROP_IMAGE: (core.crop_image, 1),
            OpCode.ROTATE_IMAGE: (core.rotate_image, 1),
            OpCode.MXMERGE: (core.max_merge_images, 2),
            OpCode.PUSH: (self.push, 0),
            OpCode.POP: (self.safe_pop, 0),
            OpCode.RET: (self.ret, 0),
            OpCode.CALL: (self.call, 0),
            OpCode.SV: (self.save, 0),
        }

    def safe_pop(self) -> Image:
        try:
            return self.img_stack.pop()
        except IndexError:
            raise ValueError(f"Stack is empty: {self.instruction_ptr}")

    def get_var(self, var: str) -> Image:
        if not (img := self.variables.get(var)):
            raise ValueError(f"Unknown variable {var}")

        return img