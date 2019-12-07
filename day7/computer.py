import itertools
import sys
from abc import abstractmethod

from day7.input import INSTRUCTIONS


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
        self.cursor = 0

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
            elif raw[0] == 99:
                return
            else:
                print(f'WARNING: {self.cursor} {raw}')
                self.cursor += 1
                continue

            cursor_move = instruction.execute(raw[1])
            self.cursor = (
                cursor_move if cursor_move is not None else self.cursor + len(instruction))

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
                                    int(parameters[0] * parameters[1]))

    def __len__(self):
        return 4


class InputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> None:
        self._computer.update_value(self._computer.read_value(self._start_position + 1),
                                    permutation[computers.index(
                                        self._computer)] if self._computer in first_values
                                    else last_output)

        if self._computer in first_values:
            first_values.remove(self._computer)

    def __len__(self):
        return 2


class OutputInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> None:
        parameters = generate_parameters(self._computer, self._start_position, modes, 1)
        global last_output, highest_output, highest_series
        last_output = parameters[0]
        if last_output > highest_output:
            highest_output = last_output
            highest_series = permutation

    def __len__(self):
        return 2


class JumpIfTrueInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> int:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        return parameters[1] if parameters[0] != 0 else None

    def __len__(self):
        return 3


class JumpIfFalseInstruction(Instruction):

    def __init__(self, computer: Computer, start_position: int):
        self._computer = computer
        self._start_position = start_position

    def execute(self, modes: [bool]) -> int:
        parameters = generate_parameters(self._computer, self._start_position, modes, 2)
        return parameters[1] if parameters[0] == 0 else None

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
    highest_output = 0
    highest_series = []

    for permutation in itertools.permutations([i for i in range(5, 10)]):
        last_output = 0
        instructions: [int] = INSTRUCTIONS
        computers: [Computer] = [Computer(instructions.copy()) for _ in
                                 range(0, len(permutation))]
        next_computer = computers[0]
        first_values = computers.copy()
        inputs = {}
        start = True
        while start or len(inputs) > 0:
            start = False
            for computer in computers:
                if computer in first_values:
                    request = computer.execute()
                    temp = last_output
                    last_output = permutation[computers.index(computer)]
                    request[0].execute([request[1][1]])
                    executed = computer.execute()
                    last_output = temp
                    inputs[computers.index(computer)] = executed
                else:
                    inputs[computers.index(computer)][0].execute(
                        inputs[computers.index(computer)][1][1])
                    temp = computer.execute()
                    if temp:
                        inputs[computers.index(computer)] = temp
                    else:
                        del inputs[computers.index(computer)]

print(highest_output)
print(highest_series)
