import sys
from abc import abstractmethod


def generate_parameters(computer: 'Computer', start: int, modes: [bool], count: int):
    return [computer.read_value(computer.read_value(start + 1 + j))
            if j >= len(modes) or modes[j] == 0
            else computer.read_value(start + 1 + j)
            if modes[j] == 1 else get_relative(computer, start, j)
            for j in range(0, count)]


def get_relative(computer: 'Computer', start, j):
    return computer.read_value(computer.relative + computer.read_value(start + 1 + j))


def parse_raw(instruction: int) -> (int, [int]):
    string = str(instruction)
    value = int(string[-2:]) if len(string) > 1 else int(string[:2])
    modes: [int] = []
    for j in range(0, len(string) - 2):
        modes.append(int(string[len(string) - 3 - j]))
    return value, modes


class Instruction:

    @abstractmethod
    def execute(self, modes: [int]):
        pass

    @abstractmethod
    def __len__(self):
        pass


class Computer:

    def __init__(self, instructions: [int], input_handle, output_handle, debug=False, relative=0,
                 cursor=0):
        self._instructions = instructions

        self.relative = relative
        self.cursor = cursor

        self.input_handle = input_handle
        self.output_handle = output_handle

        self.debug = debug

    def execute(self, wait_input=False):
        while self.cursor < len(self._instructions):
            raw = parse_raw(self._instructions[self.cursor])
            if raw[0] == 1:
                instruction = AddInstruction(self, self.cursor)
            elif raw[0] == 2:
                instruction = MultiplyInstruction(self, self.cursor)
            elif raw[0] == 3:
                instruction = InputInstruction(self, self.cursor, self.input_handle)
                if wait_input:
                    self.cursor += len(instruction)
                    return instruction, raw[1]
            elif raw[0] == 4:
                instruction = OutputInstruction(self, self.cursor, self.output_handle)
            elif raw[0] == 5:
                instruction = JumpIfTrueInstruction(self, self.cursor)
            elif raw[0] == 6:
                instruction = JumpIfFalseInstruction(self, self.cursor)
            elif raw[0] == 7:
                instruction = LessThanInstruction(self, self.cursor)
            elif raw[0] == 8:
                instruction = EqualsInstructions(self, self.cursor)
            elif raw[0] == 9:
                instruction = AdjustRelativeInstruction(self, self.cursor)
            elif raw[0] == 99:
                if self.debug:
                    print('Bye!')
                    print(self)
                return
            else:
                print(f'ERROR: could not read: {self.cursor} {raw}')
                if self.debug:
                    print(self)
                sys.exit()

            if self.debug:
                print(f'Executing: {instruction} at {self.cursor}')

            cursor_move = instruction.execute(raw[1])
            self.cursor = (
                cursor_move if cursor_move is not None else self.cursor + len(instruction))
        if self.debug:
            print(self)

    def read_value(self, position: int) -> int:
        if position < 0:
            print(f'ERROR: tried to access invalid slot: {position}')
            sys.exit()

        if position < len(self._instructions):
            return self._instructions[position]
        else:
            return 0

    def update_value(self, position: int, value_position: int) -> None:
        if position < 0:
            print(f'ERROR: tried to access invalid slot: {position}')
            sys.exit()
        if position >= len(self._instructions):
            self._instructions.extend([0 for _ in range(0, position - len(self._instructions) + 1)])

        if self.debug:
            print(f'Updating: {position} -> {value_position}')

        self._instructions[position] = value_position

    def copy(self):
        return Computer(self._instructions.copy(), self.input_handle, self.output_handle,
                        self.debug, self.relative, self.cursor)

    def __str__(self):
        return str(self._instructions)


class AddInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(
            self._computer.read_value(self._start_position + 3)
            if len(modes) < 3 or modes[2] != 2
            else self._computer.relative + self._computer.read_value(self._start_position + 3),
            parameters[0] + parameters[1])

    def __len__(self):
        return 4


class MultiplyInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(
            self._computer.read_value(self._start_position + 3)
            if len(modes) < 3 or modes[2] != 2
            else self._computer.relative + self._computer.read_value(self._start_position + 3),
            int(parameters[0] * parameters[1]))

    def __len__(self):
        return 4


class InputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int, input_handle):
        self._computer = computer
        self._start_position = start_position
        self.input_handle = input_handle

    def execute(self, modes: [int]) -> None:
        position = self._computer.read_value(self._start_position + 1) \
            if len(modes) == 0 or modes[0] != 2 else \
            self._computer.relative + self._computer.read_value(self._start_position + 1)
        self._computer.update_value(position, self.input_handle())

    def copy(self):
        return InputInstruction(self._computer.copy(), self._start_position, self.input_handle)

    def __len__(self):
        return 2


class OutputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int, output_handle):
        self._computer = computer
        self._start_position = start_position
        self.output_handle = output_handle

    def execute(self, modes: [int]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 1)
        self.output_handle(parameters[0])

    def __len__(self):
        return 2


class JumpIfTrueInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> int:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        return parameters[1] if parameters[0] != 0 else None

    def __len__(self):
        return 3


class JumpIfFalseInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> int:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        return parameters[1] if parameters[0] == 0 else None

    def __len__(self):
        return 3


class LessThanInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]):
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(
            self._computer.read_value(self._start_position + 3)
            if len(modes) < 3 or modes[2] != 2
            else self._computer.relative + self._computer.read_value(self._start_position + 3),
            1 if parameters[0] < parameters[1] else 0)

    def __len__(self):
        return 4


class EqualsInstructions(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]):
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(
            self._computer.read_value(self._start_position + 3)
            if len(modes) < 3 or modes[2] != 2
            else self._computer.relative + self._computer.read_value(self._start_position + 3),
            1 if parameters[0] == parameters[1] else 0)

    def __len__(self):
        return 4


class AdjustRelativeInstruction(Instruction):
    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]):
        parameters = generate_parameters(self._computer, self._start_position, modes, 1)
        self._computer.relative += parameters[0]

    def __len__(self):
        return 2


class ExitInstruction(Instruction):

    def __init__(self, computer: Computer):
        self._computer = computer

    def execute(self, modes: [int]):
        print(self._computer)
        sys.exit()

    def __len__(self):
        return 1


class Cell:
    value = None

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value
