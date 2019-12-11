import sys
from abc import abstractmethod

from day11.input import INSTRUCTIONS


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

    def __init__(self, instructions: [int]):
        self._instructions = instructions
        self.registers: {int: int} = {}
        self.relative = 0

    def execute(self):
        cursor: int = 0
        run: bool = True
        while cursor < len(instructions) and run:
            raw = parse_raw(instructions[cursor])
            if raw[0] == 1:
                instruction = AddInstruction(self, cursor)
            elif raw[0] == 2:
                instruction = MultiplyInstruction(self, cursor)
            elif raw[0] == 3:
                instruction = InputInstruction(self, cursor)
            elif raw[0] == 4:
                instruction = OutputInstruction(self, cursor)
            elif raw[0] == 5:
                instruction = JumpIfTrueInstruction(self, cursor)
            elif raw[0] == 6:
                instruction = JumpIfFalseInstruction(self, cursor)
            elif raw[0] == 7:
                instruction = LessThanInstruction(self, cursor)
            elif raw[0] == 8:
                instruction = EqualsInstructions(self, cursor)
            elif raw[0] == 9:
                instruction = AdjustRelativeInstruction(self, cursor)
            elif raw[0] == 99:
                print('Bye!')
                print(computer)
                return
            else:
                print(f'WARNING: {cursor} {raw}')
                cursor += 1
                continue

            cursor_move = instruction.execute(raw[1])
            cursor = (cursor_move if cursor_move is not None else cursor + len(instruction))
        print(self)

    def read_value(self, position: int) -> int:
        if position < 0:
            print(f'ERROR: tried to access invalid slot: {position}')
            return 0

        if position < len(self._instructions):
            return self._instructions[position]
        else:
            return 0

    def update_value(self, position: int, value_position: int) -> None:
        if position < 0:
            print(f'ERROR: tried to access invalid slot: {position}')
            return
        if position >= len(self._instructions):
            self._instructions.extend([0 for _ in range(0, position - len(self._instructions) + 1)])

        self._instructions[position] = value_position

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

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> None:
        value = self._computer.read_value(self._start_position + 1) \
            if len(modes) == 0 or modes[0] != 2 else \
            self._computer.relative + self._computer.read_value(self._start_position + 1)
        color = painted[location] if location in painted else 0
        self._computer.update_value(value, color)

    def __len__(self):
        return 2


class OutputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> None:
        global mode

        parameters = generate_parameters(self._computer, self._start_position, modes, 1)
        if mode == 0:
            paint(parameters[0])
            mode = 1
        else:
            move(parameters[0])
            mode = 0

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


def paint(color: int):
    painted[location] = color


def move(rotation: int):
    global direction, location

    if rotation == 0:
        direction = (direction - 1) % 4
    elif rotation == 1:
        direction = (direction + 1) % 4

    if direction == 0:
        location = (location[0], location[1] + 1)
    elif direction == 1:
        location = (location[0] + 1, location[1])
    elif direction == 2:
        location = (location[0], location[1] - 1)
    elif direction == 3:
        location = (location[0] - 1, location[1])
    else:
        print('ERROR')


def num_plate():
    min_x = min([loc[0] for loc in painted])
    max_x = max([loc[0] for loc in painted])
    min_y = min([loc[1] for loc in painted])
    max_y = max([loc[1] for loc in painted])

    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            if (x, y) in painted:
                if painted[(x, y)] == 1:
                    line += '*'
                else:
                    line += '-'
            else:
                line += '-'
        print(line)


if __name__ == '__main__':
    instructions: [int] = INSTRUCTIONS
    computer: Computer = Computer(instructions)
    painted = {(0, 0): 1}
    mode = 0
    location = (0, 0)
    direction = 0
    computer.execute()
    print(len(painted))
    num_plate()
