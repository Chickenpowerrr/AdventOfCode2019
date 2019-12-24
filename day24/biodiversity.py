ACTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))


class Grid:

    def __init__(self, bugs: {(int, int): bool}):
        self.bugs = bugs

    def next_state(self):
        next_bugs = self.bugs.copy()
        for position in self.bugs:
            adjacent = self._get_adjacent(position)
            if self.bugs[position]:
                next_bugs[position] = (adjacent == 1)
            else:
                next_bugs[position] = (0 < adjacent <= 2)
        self.bugs = next_bugs

    def get_biodiversity(self):
        max_x = max([position[0] for position in self.bugs]) + 1
        return sum([pow(2, max_x * position[1] + position[0])
                    for position in self.bugs if self.bugs[position]])

    def _get_adjacent(self, position: (int, int)):
        adjacent_count = 0
        for action in ACTIONS:
            cursor = position[0] + action[0], position[1] + action[1]
            if cursor in self.bugs and self.bugs[cursor]:
                adjacent_count += 1
        return adjacent_count

    def render(self):
        for y in range(max([position[1] for position in self.bugs]) + 1):
            line = ''
            for x in range(max([position[0] for position in self.bugs]) + 1):
                if self.bugs[(x, y)]:
                    line += '#'
                else:
                    line += '.'
            print(line)


class RecursiveGrid:

    def __init__(self, bugs: {(int, int): bool}, center: (int, int),
                 inner_bugs: {(int, int): {(int, int)}} = None,
                 outer_bugs: {(int, int): {(int, int)}} = None,
                 higher_layer: 'RecursiveGrid' = None, lower_layer: 'RecursiveGrid' = None):

        self.bugs = bugs
        self.center = center
        self.higher_layer = higher_layer
        self.lower_layer = lower_layer
        self.next_bugs = {}

        if not inner_bugs:
            self.inner_bugs = {}
            max_x = max([position[0] for position in self.bugs])
            max_y = max([position[1] for position in self.bugs])

            self.inner_bugs[center[0], center[1] - 1] = [position for position in bugs
                                                         if position[1] == 0]
            self.inner_bugs[center[0] + 1, center[1]] = [position for position in bugs
                                                         if position[0] == max_x]
            self.inner_bugs[center[0], center[1] + 1] = [position for position in bugs
                                                         if position[1] == max_y]
            self.inner_bugs[center[0] - 1, center[1]] = [position for position in bugs
                                                         if position[0] == 0]
        else:
            self.inner_bugs = inner_bugs

        if not outer_bugs:
            self.outer_bugs = {}
            for position in self.inner_bugs:
                for inner_position in self.inner_bugs[position]:
                    if inner_position not in self.outer_bugs:
                        self.outer_bugs[inner_position] = {position}
                    else:
                        self.outer_bugs[inner_position].add(position)
        else:
            self.outer_bugs = outer_bugs

    def _get_adjacent(self, position: (int, int)):
        adjacent_count = 0
        # Within own grid
        for action in ACTIONS:
            cursor = position[0] + action[0], position[1] + action[1]
            if cursor in self.bugs and self.bugs[cursor]:
                adjacent_count += 1

        # Upper grid
        if self.higher_layer and position in self.outer_bugs:
            for outer_position in self.outer_bugs[position]:
                if self.higher_layer.bugs[outer_position]:
                    adjacent_count += 1

        # Lower grid
        if self.lower_layer and position in self.inner_bugs:
            for inner_position in self.inner_bugs[position]:
                if self.lower_layer.bugs[inner_position]:
                    adjacent_count += 1

        return adjacent_count

    def next_state(self):
        next_bugs = self.bugs.copy()
        for position in self.bugs:
            adjacent = self._get_adjacent(position)
            if self.bugs[position]:
                next_bugs[position] = (adjacent == 1)
            else:
                next_bugs[position] = (0 < adjacent <= 2)
        self.next_bugs = next_bugs

    def finalize_next_state(self) -> {'RecursiveGrid'}:
        self.bugs = self.next_bugs
        self.next_bugs = {}

        next_grids = set()
        if not self.lower_layer:
            next_grid = RecursiveGrid({position: False for position in self.bugs}, self.center,
                                      self.inner_bugs, self.outer_bugs, self, None)
            next_grids.add(next_grid)
            self.lower_layer = next_grid
        if not self.higher_layer:
            next_grid = RecursiveGrid({position: False for position in self.bugs}, self.center,
                                      self.inner_bugs, self.outer_bugs, None, self)
            next_grids.add(next_grid)
            self.higher_layer = next_grid
        return next_grids

    def get_bug_count(self):
        return len([position for position in self.bugs if self.bugs[position]])

    def render(self):
        for y in range(max([position[1] for position in self.bugs]) + 1):
            line = ''
            for x in range(max([position[0] for position in self.bugs]) + 1):
                if (x, y) != self.center:
                    if self.bugs[(x, y)]:
                        line += '#'
                    else:
                        line += '.'
                else:
                    line += '?'
            print(line)


def load_grid():
    bugs = {}
    with open('input.txt') as file:
        y = 0
        for line in file.readlines():
            line = line.strip()
            for x in range(len(line)):
                bugs[(x, y)] = (line[x] == '#')
            y += 1
    return Grid(bugs)


def load_recursive_grid():
    bugs = load_grid().bugs
    max_x = max([position[0] for position in bugs])
    max_y = max([position[1] for position in bugs])
    center = (max_x // 2, max_y // 2)
    del bugs[center]

    higher = RecursiveGrid({position: False for position in bugs}, center)
    lower = RecursiveGrid({position: False for position in bugs}, center)
    current = RecursiveGrid(bugs, center, higher_layer=higher, lower_layer=lower)
    higher.lower_layer = current
    lower.higher_layer = current
    return current


def part1():
    grid = load_grid()
    history = []

    while grid.bugs not in history:
        history.append(grid.bugs)
        grid.next_state()

    print(f'Biodiversity for the first reappearing grid: {grid.get_biodiversity()}')


def part2():
    start_grid = load_recursive_grid()
    grids = [start_grid, start_grid.lower_layer, start_grid.higher_layer]

    for _ in range(200):
        for grid in grids:
            grid.next_state()
        next_grids = grids.copy()
        for grid in grids:
            next_grids.extend(grid.finalize_next_state())
        grids = next_grids

    print(f'Bugs after 200 minutes: {sum([grid.get_bug_count() for grid in grids])}')


if __name__ == '__main__':
    part1()
    part2()
