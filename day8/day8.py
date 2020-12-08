import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/8/input'


class InstructionAlreadyRunException(Exception):
    def __init__(self, accumulator_value):
        self.accumulator_value = accumulator_value


class HandHeld(object):
    """
    Simulator for a handheld console's instruction boot sequence

    Takes the raw text for a set of instructions and parses it.

    Maintains an instruction pointer, which is the index of the current instruction.

    To ensure instructions aren't repeated, as they're executed the pointer is added
    to the list of executed instructions. If an instruction is repeated, raise the
    custom exception type, with the accumulator value as an argument.
    """

    def __init__(self):
        self.instructions = []
        self.instruction_ptr = 0

        self.executed = []

        self.accumulator = 0

    def startup(self):
        if len(self.instructions) == 0:
            raise ReferenceError("Instruction set is empty - have you run the parser?")
        while self.instruction_ptr < len(self.instructions):
            if self.instruction_ptr in self.executed:
                raise InstructionAlreadyRunException(self.accumulator)
            self.execute()

    def execute(self):
        self.executed.append(self.instruction_ptr)
        instruction_fn, arg = self.instructions[self.instruction_ptr]
        instruction_fn(arg)

    def nop(self, arg):
        self.instruction_ptr += 1

    def acc(self, arg):
        self.instruction_ptr += 1
        self.accumulator += arg

    def jmp(self, arg):
        self.instruction_ptr += arg

    def parse_instructions(self, raw_input):
        functions = {
            "nop": self.nop,
            "acc": self.acc,
            "jmp": self.jmp
        }
        for line in raw_input.split("\n"):
            line = line.strip()
            if line == "":
                continue

            fn_name, arg = line.split()
            fn = functions[fn_name.strip()]
            self.instructions.append((fn, int(arg.strip())))


def task_1(data):
    hh = HandHeld()
    hh.parse_instructions(data)
    try:
        hh.startup()
    except InstructionAlreadyRunException as err:
        print(f"The accumulator is {err.accumulator_value}")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    task_1(input_data)
