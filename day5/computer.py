import sys
from abc import abstractmethod

from day5.input import INSTRUCTIONS


def generate_parameters(computer: 'Computer', start: int, modes: [bool], count: int):
    return [computer.read_value(
        computer.read_value(start + 1 + j)) if j >= len(modes) or modes[j] == 0
            else computer.read_value(start + 1 + j) for j in range(0, count)]


def parse_raw(instruction: int) -> (int, [bool]):
    string = str(instruction)
    value = int(string[-2:]) if len(string) > 1 else int(string[:2])
    modes: [bool] = []
    for j in range(0, len(string) - 2):
        modes.append(string[len(string) - 3 - j] == '1')
    return value, modes


class Instruction:

    @abstractmethod
    def execute(self, modes: [bool]):
        pass

    @abstractmethod
    def __len__(self):
        pass


class Computer:

    def __init__(self, instructions: [int]):
        self._instructions = instructions
        self.registers: {int: int} = {}

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
            elif raw[0] == 99:
                print('Bye!')
                print(computer)
                return
            else:
                print(f'WARNING: {cursor} {raw}')
                cursor += 1
                continue

            cursor_move = instruction.execute(raw[1])
            cursor = (cursor_move if cursor_move else cursor + len(instruction))
        print(self)

    def read_value(self, position: int) -> int:
        return self._instructions[position]

    def update_value(self, position: int, value_position: int) -> None:
        self._instructions[position] = value_position

    def __str__(self):
        return str(self._instructions)


class AddInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(self._computer.read_value(self._start_position + 3),
                                    parameters[0] + parameters[1])

    def __len__(self):
        return 4


class MultiplyInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(self._computer.read_value(self._start_position + 3),
                                    parameters[0] * parameters[1])

    def __len__(self):
        return 4


class InputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> None:
        self._computer.update_value(self._computer.read_value(self._start_position + 1),
                                    int(input('Please enter a number: ')))

    def __len__(self):
        return 2


class OutputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 1)
        print(f'> {parameters[0]}')

    def __len__(self):
        return 2


class JumpIfTrueInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> int:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        return parameters[1] if parameters[0] != 0 else 0

    def __len__(self):
        return 3


class JumpIfFalseInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> int:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        return parameters[1] if parameters[0] == 0 else 0

    def __len__(self):
        return 3


class LessThanInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]):
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(self._computer.read_value(self._start_position + 3),
                                    1 if parameters[0] < parameters[1] else 0)

    def __len__(self):
        return 4


class EqualsInstructions(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]):
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        self._computer.update_value(self._computer.read_value(self._start_position + 3),
                                    1 if parameters[0] == parameters[1] else 0)

    def __len__(self):
        return 4


class ExitInstruction(Instruction):

    def __init__(self, computer: Computer):
        self._computer = computer

    def execute(self, modes: [bool]):
        print(self._computer)
        sys.exit()

    def __len__(self):
        return 1


if __name__ == '__main__':
    instructions: [int] = INSTRUCTIONS
    computer: Computer = Computer(instructions)
    computer.execute()
