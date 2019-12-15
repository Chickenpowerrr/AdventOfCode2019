import sys

from day11.input import INSTRUCTIONS
from intcode.computer import Computer


class Cursor:

    def __init__(self, start_color: int):
        self.painted = {(0, 0): start_color}
        self.mode = 0
        self.location = (0, 0)
        self.direction = 0

    def handle_input(self) -> int:
        return self.painted[self.location] if self.location in self.painted else 0

    def handle_output(self, value: int) -> None:
        if self.mode == 0:
            self.painted[self.location] = value
            self.mode = 1
        else:
            self.move(value)
            self.mode = 0

    def move(self, rotation: int) -> None:
        if rotation == 0:
            self.direction = (self.direction - 1) % 4
        elif rotation == 1:
            self.direction = (self.direction + 1) % 4

        if self.direction == 0:
            self.location = (self.location[0], self.location[1] + 1)
        elif self.direction == 1:
            self.location = (self.location[0] + 1, self.location[1])
        elif self.direction == 2:
            self.location = (self.location[0], self.location[1] - 1)
        elif self.direction == 3:
            self.location = (self.location[0] - 1, self.location[1])
        else:
            print(f'ERROR: found direction {self.direction}')
            sys.exit()


def get_painted(start_position: int):
    instructions: [int] = INSTRUCTIONS.copy()
    cursor: Cursor = Cursor(start_position)
    computer: Computer = Computer(instructions, cursor.handle_input, cursor.handle_output)
    computer.execute()
    return cursor.painted


def part1():
    print(f'Painted panels: {len(get_painted(0))}')


def part2():
    painted = get_painted(1)

    min_x = min([loc[0] for loc in painted])
    max_x = max([loc[0] for loc in painted])
    min_y = min([loc[1] for loc in painted])
    max_y = max([loc[1] for loc in painted])

    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            if (x, max_y - y + min_y) in painted:
                if painted[(x, max_y - y + min_y)] == 1:
                    line += '*'
                else:
                    line += '-'
            else:
                line += '-'
        print(line)


if __name__ == '__main__':
    part1()
    part2()
