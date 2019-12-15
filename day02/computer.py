from day02.input import INSTRUCTIONS
from intcode.computer import Computer


def part1():
    instructions: [int] = INSTRUCTIONS.copy()
    instructions[1] = 12
    instructions[2] = 2
    computer: Computer = Computer(instructions, lambda: int(input('Please enter a number')),
                                  lambda output: print(f'> {output}'))
    computer.execute()
    print(f'Value at position 0: {instructions[0]}')


def part2():
    for i in range(0, 100):
        for j in range(0, 100):
            instructions: [int] = INSTRUCTIONS.copy()
            instructions[1] = i
            instructions[2] = j
            computer: Computer = Computer(instructions, lambda: int(input('Please enter a number')),
                                          lambda output: print(f'> {output}'))
            computer.execute()
            if instructions[0] == 19690720:
                print(f'100 * {i} + {j} = {100 * i + j}')
                return


if __name__ == '__main__':
    part1()
    part2()
