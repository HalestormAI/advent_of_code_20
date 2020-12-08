import pathlib
import sys
from collections import deque

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

    def reset(self):
        self.accumulator = 0
        self.executed = []
        self.instruction_ptr = 0

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


class Task2HandHeld(HandHeld):
    """
    Greedy search through the possible jumps we can replace, not super efficient but it'll work.

    When we parse the instructions, create a clone of the instruction set, and create a queue of all
    the `jmp` instructions.

    When we we hit a repeated instruction, reset the instruction set (and accumulator and ptr) back
    to the original, pop the last `jmp` off the queue and replace it with a `nop`. Try to startup again.

    If we still get a repeated instruction, reset again, take the next jump, etc. Repeat ad nauseam.
    """

    def __init__(self):
        super().__init__()

        self._original_instructions = None
        self._jumps_to_test = None

    def parse_instructions(self, raw_input):
        super(Task2HandHeld, self).parse_instructions(raw_input)
        self._original_instructions = self.instructions.copy()
        self._jumps_to_test = deque([i for i, f in enumerate(self.instructions) if f[0] == self.jmp])

    def startup(self):
        if len(self.instructions) == 0:
            raise ReferenceError("Instruction set is empty - have you run the parser?")

        while self.instruction_ptr < len(self.instructions):
            if self.instruction_ptr in self.executed:
                if len(self._jumps_to_test) > 0:
                    self.reset()
                    jmp_id = self._jumps_to_test.pop()
                    self.instructions[jmp_id] = (self.nop, None)
                    print(f"Swapping jump {jmp_id} for a nop")
                else:
                    raise InstructionAlreadyRunException(self.accumulator)
            self.execute()

    def reset(self):
        super(Task2HandHeld, self).reset()
        self.instructions = self._original_instructions.copy()


def task_1(data):
    hh = HandHeld()
    hh.parse_instructions(data)
    try:
        hh.startup()
    except InstructionAlreadyRunException as err:
        print(f"The accumulator is {err.accumulator_value}")


def task_2(data):
    hh = Task2HandHeld()
    hh.parse_instructions(data)
    try:
        hh.startup()
        print(f"Final accumulator was: {hh.accumulator}")
    except InstructionAlreadyRunException as err:
        print(f"Mission failed - The accumulator is {err.accumulator_value}")


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')

    print("Task 1")
    task_1(input_data)

    print()
    print("Task 2")
    task_2(input_data)
