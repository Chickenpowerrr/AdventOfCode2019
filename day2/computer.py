import sys
from abc import abstractmethod

from day2.input import INSTRUCTIONS


class Instruction:

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def __len__(self):
        pass


class Computer:

    def __init__(self, instructions: [int]):
        self._instructions = instructions

    def execute(self):
        cursor: int = 0
        run: bool = True
        while cursor < len(instructions) and run:
            if instructions[cursor] == 1:
                instruction = AddInstruction(self, cursor)
            elif instructions[cursor] == 2:
                instruction = MultiplyInstruction(self, cursor)
            elif instructions[cursor] == 99:
                return
            else:
                print('ERROR!')
                sys.exit()
            cursor += len(instruction)
            instruction.execute()

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

    def execute(self) -> None:
        self._computer.update_value(self._computer.read_value(self._start_position + 3),
                                    self._computer.read_value(self._computer.read_value(
                                        self._start_position + 1)) + self._computer.read_value(
                                        self._computer.read_value(self._start_position + 2)))

    def __len__(self):
        return 4


class MultiplyInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self) -> None:
        self._computer.update_value(self._computer.read_value(self._start_position + 3),
                                    self._computer.read_value(self._computer.read_value(
                                        self._start_position + 1)) * self._computer.read_value(
                                        self._computer.read_value(self._start_position + 2)))

    def __len__(self):
        return 4


class ExitInstruction(Instruction):

    def __init__(self, computer: Computer):
        self._computer = computer

    def execute(self):
        print(self._computer)
        sys.exit()

    def __len__(self):
        return 1


if __name__ == '__main__':
    for i in range(0, 100):
        for j in range(0, 100):
            instructions: [int] = INSTRUCTIONS.copy()
            instructions[1] = i
            instructions[2] = j
            computer: Computer = Computer(instructions)
            computer.execute()
            if instructions[0] == 19690720:
                print(f'Found: {i} {j}')
