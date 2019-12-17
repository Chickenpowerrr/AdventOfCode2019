from enum import Enum, IntEnum

from day17.input import INSTRUCTIONS
from intcode.computer import Computer


class Board:

    def __init__(self):
        self.filled = {}
        self.cursor = (0, 0)
        self.max_x = 0
        self.min_y = 0
        self.input = None

    def fill(self, value: int):
        if value != 10:
            self.filled[self.cursor] = value

            if self.max_x < self.cursor[0]:
                self.max_x = self.cursor[0]

            if self.min_y > self.cursor[1]:
                self.min_y = self.cursor[1]

            self.cursor = (self.cursor[0] + 1, self.cursor[1])
        else:
            self.cursor = (0, self.cursor[1] - 1)

    def intersections(self, value: int) -> (int, int):
        result = set()
        for location in self.filled:
            if (location[0] + 1, location[1]) in self.filled and \
                    (location[0] - 1, location[1]) in self.filled and \
                    (location[0], location[1] + 1) in self.filled and \
                    (location[0], location[1] - 1) in self.filled and \
                    value == self.filled[location] == \
                    self.filled[(location[0] + 1, location[1])] == \
                    self.filled[(location[0] - 1, location[1])] == \
                    self.filled[(location[0], location[1] + 1)] == \
                    self.filled[(location[0], location[1] - 1)] == value:
                result.add(location)
        return result

    def value(self, intersection: (int, int)) -> int:
        return abs(intersection[0] * intersection[1])

    def render(self):
        for y in range(0, self.min_y - 1, -1):
            line = '.'
            for x in range(self.max_x + 1):
                line += str(chr(self.filled[(x, y)]))
            print(line)


def get_board():
    board: Board = Board()
    instructions = INSTRUCTIONS.copy()
    computer: Computer = Computer(instructions, lambda: int(input('Please enter a number ')),
                                  board.fill)
    computer.execute()
    return board


def part1():
    board = get_board()
    print(f'Alignment parameters: '
          f'{sum({board.value(intersection) for intersection in board.intersections(35)})}')


def part2():
    board = get_board()
    # Render to solve it with pen and paper
    board.render()


if __name__ == '__main__':
    part1()
