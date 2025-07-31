import re

from .constants import OpCode
from .models import Instruction


class Parser:
    def __init__(self):
        self.opcode_pattern = re.compile(r'^[A-Z][A-Z0-9]{1,7}$')
        self.quoted_string_pattern = re.compile(r'^"([^"\\]*(?:\\.[^"\\]*)*)"')
        self.single_quoted_string_pattern = re.compile(r"^'([^'\\]*(?:\\.[^'\\]*)*)'")
        self.int_pattern = re.compile(r'^-?\d+$')
        self.float_pattern = re.compile(r'^-?\d+\.\d+$')

    def parse_text(self, text: str) -> list[Instruction]:
        instructions = []
        lines = self._preprocess_text(text)

        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue

            try:
                instruction = self._parse_line(line)
                instructions.append(instruction)
            except ValueError as e:
                raise ValueError(f"Line {line_num}: {str(e)}") from e

        return instructions

    def _preprocess_text(self, text: str) -> list[str]:
        return [line.strip() for line in text.split('\n') if line.strip()]

    def _parse_line(self, line: str) -> Instruction:
        parts = self._split_line(line)
        if not parts:
            raise ValueError("Empty instruction")

        try:
            opcode = OpCode(parts[0])
        except ValueError:
            raise ValueError(f"Invalid opcode: '{parts[0]}'")

        parsed_args = []
        for arg in parts[1:]:
            parsed_args.append(self._parse_arg(arg))

        return Instruction(opcode, tuple(parsed_args))

    def _split_line(self, line: str) -> list[str]:
        tokens = []
        current_token = []
        in_quotes = None
        escape = False

        for c in line:
            if escape:
                current_token.append(c)
                escape = False
                continue

            if c == '\\':
                escape = True
                continue

            if in_quotes:
                current_token.append(c)
                if c == in_quotes:
                    in_quotes = None
                    tokens.append(''.join(current_token))
                    current_token = []
            else:
                if c in ('"', "'"):
                    if current_token:
                        tokens.append(''.join(current_token))
                        current_token = []
                    in_quotes = c
                    current_token.append(c)
                elif c.isspace():
                    if current_token:
                        tokens.append(''.join(current_token))
                        current_token = []
                else:
                    current_token.append(c)

        if current_token:
            tokens.append(''.join(current_token))

        if in_quotes:
            raise ValueError("Unterminated quoted string")

        return [token.strip() for token in tokens if token.strip()]

    def _parse_arg(self, arg: str) -> float | int | str:
        if arg.startswith('"') and arg.endswith('"'):
            return arg[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        if arg.startswith("'") and arg.endswith("'"):
            return arg[1:-1].replace("\\'", "'").replace("\\\\", "\\")

        if self.int_pattern.match(arg):
            return int(arg)
        if self.float_pattern.match(arg):
            return float(arg)

        return arg