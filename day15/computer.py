import itertools
import sys
from abc import abstractmethod

import numpy

from day15.input import INSTRUCTIONS


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

    def __init__(self, instructions: [int], cursor=0):
        self._instructions = instructions
        self.registers: {int: int} = {}
        self.relative = 0
        self.cursor = cursor
        self.status = 1

    def execute(self):
        run: bool = True
        while self.cursor < len(self._instructions) and run:
            raw = parse_raw(self._instructions[self.cursor])
            if raw[0] == 1:
                instruction = AddInstruction(self, self.cursor)
            elif raw[0] == 2:
                instruction = MultiplyInstruction(self, self.cursor)
            elif raw[0] == 3:
                instruction = InputInstruction(self, self.cursor)
                self.cursor += len(instruction)
                return instruction, raw
            elif raw[0] == 4:
                instruction = OutputInstruction(self, self.cursor)
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
                return
            else:
                print(f'WARNING: {self.cursor} {raw}')
                sys.exit()
            cursor_move = instruction.execute(raw[1])
            self.cursor = (
                cursor_move if cursor_move is not None else self.cursor + len(instruction))
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

    def copy(self):
        return Computer(self._instructions.copy(), self.cursor)

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

    def execute(self, modes: [int], position: (int, int), value: int) -> (int, int):
        pos = self._computer.read_value(self._start_position + 1) \
            if len(modes) == 0 or modes[0] != 2 else \
            self._computer.relative + self._computer.read_value(self._start_position + 1)

        self._computer.update_value(pos, value)

        if value == 1:
            return position[0], position[1] + 1
        elif value == 2:
            return position[0], position[1] - 1
        elif value == 3:
            return position[0] - 1, position[1]
        elif value == 4:
            return position[0] + 1, position[1]

    def copy(self):
        return InputInstruction(self._computer.copy(), self._start_position)

    def __len__(self):
        return 2


class OutputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [int]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 1)
        self._computer.status = parameters[0]

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


class Path:

    def __init__(self, path: {(int, int)}, current: (int, int), instruction: InputInstruction,
                 modes, done=False):
        self.path = path
        self.current = current
        self.instruction = instruction
        self.done = done
        self.modes = modes

    def get_next(self):
        coming = []
        for i in range(4):
            attempt = self.instruction.copy()
            pos = attempt.execute(self.modes, self.current, i + 1)
            request = attempt._computer.execute()
            status = attempt._computer.status
            if pos not in self.path:
                path = self.path.copy()
                path.add(pos)
                if status == 1:
                    coming.append(Path(path, pos, request[0], request[1]))
                elif status == 2:
                    coming.append(Path(path, pos, request[0], request[1], True))
        return coming

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return f'{self.current}, {self.done}, {self.path}'


class Oxygen:

    def __init__(self, filled: {(int, int)}, current: (int, int), instruction: InputInstruction,
                 modes):
        self.filled = filled
        self.current = current
        self.instruction = instruction
        self.modes = modes

    def get_infected(self):
        coming = []
        for i in range(4):
            attempt = self.instruction.copy()
            pos = attempt.execute(self.modes, self.current, i + 1)
            request = attempt._computer.execute()
            status = attempt._computer.status
            if pos not in self.filled:
                self.filled.add(pos)
                if status == 1:
                    coming.append(Oxygen(self.filled, pos, request[0], request[1]))
        return coming

    def __str__(self):
        return f'{self.current}'


def get_shortest_path():
    instructions: [int] = INSTRUCTIONS.copy()
    computer: Computer = Computer(instructions)
    ex = computer.execute()
    path = Path({(0, 0)}, (0, 0), ex[0], ex[1])
    paths = {0: [path]}

    min_path_len = 0
    min_path = None
    while not min_path_len or min(paths) < min_path_len:
        next_length = min(paths)
        cursors = paths[next_length]
        del paths[next_length]

        for path in cursors:
            for next_path in path.get_next():
                next_len = len(next_path)
                if not next_path.done:
                    if next_len not in paths:
                        paths[next_len] = [next_path]
                    else:
                        paths[next_len].append(next_path)
                else:
                    if not min_path_len or min_path_len > next_len:
                        min_path_len = next_len
                        min_path = next_path
    return min_path


def part1():
    print(f'Shortest: {len(get_shortest_path()) - 1}')


def part2():
    path = get_shortest_path()
    latest_oxygen = [Oxygen(set(path.current), path.current, path.instruction, path.modes)]
    minutes = 0
    while len(latest_oxygen) > 0:
        next_oxygen = set()
        for oxygen in latest_oxygen:
            for target in oxygen.get_infected():
                next_oxygen.add(target)
        latest_oxygen = next_oxygen
        minutes += 1
    print(f'Minutes expired: {minutes - 1}')


if __name__ == '__main__':
    part1()
    part2()
