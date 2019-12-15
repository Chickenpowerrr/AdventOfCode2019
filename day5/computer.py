from day5.input import INSTRUCTIONS
from intcode.computer import Computer, Cell


def part1():
    instructions: [int] = INSTRUCTIONS.copy()
    cell: Cell = Cell()
    computer: Computer = Computer(instructions, lambda: 1, lambda output: cell.set_value(output))
    computer.execute()
    print(f'Diagnostic Test Code: {cell.get_value()}')


def part2():
    instructions: [int] = INSTRUCTIONS.copy()
    cell: Cell = Cell()
    computer: Computer = Computer(instructions, lambda: 5, lambda output: cell.set_value(output))
    computer.execute()
    print(f'Diagnostic Code: {cell.get_value()}')


if __name__ == '__main__':
    part1()
    part2()
