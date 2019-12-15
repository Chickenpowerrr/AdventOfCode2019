from day15.input import INSTRUCTIONS
from intcode.computer import InputInstruction, Computer, Cell

cell: Cell = Cell()


class Path:

    def __init__(self, path: {(int, int)}, location: (int, int), instruction: InputInstruction,
                 modes, done=False):
        self.path = path
        self.location = location
        self.instruction = instruction
        self.done = done
        self.modes = modes

    def get_next(self):
        coming = []
        for i in range(1, 5):
            attempt: InputInstruction = self.instruction.copy()
            attempt.input_handle = lambda: i
            attempt.execute(self.modes)
            location = self.location

            if i == 1:
                location = location[0], location[1] + 1
            elif i == 2:
                location = location[0], location[1] - 1
            elif i == 3:
                location = location[0] - 1, location[1]
            elif i == 4:
                location = location[0] + 1, location[1]

            request = attempt._computer.execute(True)
            if location not in self.path:
                path = self.path.copy()
                path.add(location)
                if cell.value == 1:
                    coming.append(Path(path, location, request[0], request[1]))
                elif cell.value == 2:
                    coming.append(Path(path, location, request[0], request[1], True))
        return coming

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return f'{self.location}, {self.done}, {self.path}'


class Oxygen:

    def __init__(self, filled: {(int, int)}, location: (int, int), instruction: InputInstruction,
                 modes):
        self.filled = filled
        self.location = location
        self.instruction = instruction
        self.modes = modes

    def get_infected(self):
        coming = []
        for i in range(1, 5):
            attempt = self.instruction.copy()
            attempt.input_handle = lambda: i
            attempt.execute(self.modes)

            location = self.location

            if i == 1:
                location = location[0], location[1] + 1
            elif i == 2:
                location = location[0], location[1] - 1
            elif i == 3:
                location = location[0] - 1, location[1]
            elif i == 4:
                location = location[0] + 1, location[1]

            request = attempt._computer.execute(True)
            if location not in self.filled:
                self.filled.add(location)
                if cell.value == 1:
                    coming.append(Oxygen(self.filled, location, request[0], request[1]))
        return coming

    def __str__(self):
        return f'{self.location}'


def get_shortest_path():
    instructions: [int] = INSTRUCTIONS.copy()
    computer: Computer = Computer(instructions, lambda: 0, cell.set_value)
    request: (InputInstruction, [int]) = computer.execute(True)
    path = Path({(0, 0)}, (0, 0), request[0], request[1])
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
    latest_oxygen = [Oxygen(set(path.location), path.location, path.instruction, path.modes)]
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
