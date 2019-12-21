from day19.input import INSTRUCTIONS
from intcode.computer import Computer


class Beam:

    def __init__(self, diagonal: int):
        self.locations: {(int, int)} = set()
        self.diagonal = diagonal
        self.x = 0
        self.y = 0
        self.send_x = True
        self.done = False

    def handle_input(self) -> int:
        if not self.done:
            if self.send_x:
                self.send_x = False
                return self.x
            else:
                self.send_x = True
                return self.y
        else:
            return -1

    def handle_output(self, output: int):
        if output == 1:
            self.locations.add((self.x, self.y))
        if self.x == self.diagonal - 1:
            self.x = 0
            if self.y == self.diagonal - 1:
                self.done = True
            else:
                self.y += 1
        else:
            self.x += 1

    def render(self):
        for y in range(self.diagonal):
            line = ''
            for x in range(self.diagonal):
                line += '#' if (x, y) in self.locations else '.'
            print(line)


class ShipBeam:
    min_x: {int, int} = {}

    def __init__(self, diagonal: int, y: int):
        self.locations: {(int, int)} = set()
        self.diagonal = diagonal
        self.x = 0
        self.y = y
        self.send_x = True
        self.done = False
        self.finished_line = False
        self.fits = False

        y_cursor = 0
        for key in self.min_x:
            if y > key > y_cursor:
                y_cursor = key
                self.x = self.min_x[key]

    def handle_input(self) -> int:
        if self.send_x:
            self.send_x = False
            return self.x
        else:
            self.send_x = True
            return self.y

    def handle_output(self, output: int):
        updated_finished = False
        if output == 1:
            if len(self.locations) == 0:
                self.min_x[self.y] = self.x
            self.locations.add((self.x, self.y))
        elif len(self.locations) > 0:
            self.y += self.diagonal - 1
            self.x -= self.diagonal
            updated_finished = not self.finished_line
            self.finished_line = True

        if not self.finished_line:
            self.x += 1
        elif not updated_finished:
            self.done = True
            y = self.y - self.diagonal + 1
            self.fits = (self.x, self.y) in self.locations \
                        and len([coord for coord in self.locations if
                                 coord[1] == y and self.x <= coord[0]]) >= self.diagonal


def find_ship_beam_range(step_size: int, diagonal: int, start: int = 0) -> int:
    y = start
    while True:
        ship_beam: ShipBeam = ShipBeam(diagonal, y)
        while not ship_beam.done:
            instructions = INSTRUCTIONS.copy()
            computer: Computer = Computer(instructions, ship_beam.handle_input,
                                          ship_beam.handle_output)
            computer.execute()
        if ship_beam.fits:
            return y - step_size
        else:
            y += step_size


def part1():
    beam: Beam = Beam(50)
    while not beam.done:
        instructions = INSTRUCTIONS.copy()
        computer: Computer = Computer(instructions, beam.handle_input, beam.handle_output)
        computer.execute()
    print(f'Pulling on: {len(beam.locations)} points')


def part2():
    diagonal = 100
    min_search = find_ship_beam_range(20, diagonal)
    total_minimum = find_ship_beam_range(1, diagonal, min_search) + 1

    ship_beam: ShipBeam = ShipBeam(diagonal, total_minimum + diagonal)
    while not ship_beam.done:
        instructions = INSTRUCTIONS.copy()
        computer: Computer = Computer(instructions, ship_beam.handle_input,
                                      ship_beam.handle_output)
        computer.execute()
    print(f'{diagonal} x {diagonal} square corner:'
          f' {min([coord[0] - 1 for coord in ship_beam.locations]) * 10_000 + total_minimum}')


if __name__ == '__main__':
    part1()
    part2()
