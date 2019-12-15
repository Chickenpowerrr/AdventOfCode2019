from day9.input import INSTRUCTIONS
from intcode.computer import Computer, Cell


def part1():
    instructions: [int] = INSTRUCTIONS
    cell: Cell = Cell()
    computer: Computer = Computer(instructions, lambda: 1, lambda output: cell.set_value(output))
    computer.execute()
    print(f'BOOST Test keycode: {cell.get_value()}')


def part2():
    instructions: [int] = INSTRUCTIONS
    cell: Cell = Cell()
    computer: Computer = Computer(instructions, lambda: 2, lambda output: cell.set_value(output))
    computer.execute()
    print(f'BOOST keycode: {cell.get_value()}')


if __name__ == '__main__':
    part1()
    part2()
