class Line:

    def __init__(self, length: int, start: (int, int), end: (int, int), doors: {(int, int)}):
        self.length = length
        self.start = start
        self.end = end
        self.doors = doors

    def __len__(self):
        return self.length

    def __eq__(self, other):
        return isinstance(other, Line) and (self.start == other.end or self.start == other.start) \
               and (self.end == other.end or self.end == other.start)

    def __str__(self):
        return f'<start={self.start} end={self.end} length={self.length}>'


class Maze:
    ACTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}

    def __init__(self, walls=None, keys=None, doors=None, cursor=None):
        self.walls: {(int, int)} = walls if walls else set()
        self.keys: {(int, int): str} = keys if keys else {}
        self.doors: {(int, int): str} = doors if doors else {}
        self.cursor = cursor if cursor else (0, 0)
        self.lines: {(int, int): {Line}} = {}

    def obtain_key(self, location: (int, int)):
        name = self.keys[location].upper()
        self.cursor = location
        del self.keys[location]
        for door in self.doors.copy():
            if self.doors[door] == name:
                del self.doors[door]

    def _generate_lines(self, point, critical_points):
        paths = [(point, point, set(), 0)]
        result = []

        while len(paths) > 0:
            temp_paths = paths.copy()
            paths = []
            for path in temp_paths:
                for action in self.ACTIONS:
                    target = path[0][0] + action[0], path[0][1] + action[1]
                    if target not in self.walls and target != path[1]:
                        doors = path[2].copy()
                        if target in self.doors:
                            doors.add(target)

                        if target in critical_points:
                            result.append(Line(path[3] + 1, point, target, doors))
                        else:
                            paths.append((target, path[0], doors, path[3] + 1))
        return result

    def render(self):
        intersections = self.get_splits()
        for y in range(max(coord[1] for coord in self.walls) + 1):
            line = ''
            for x in range(max(coord[0] for coord in self.walls) + 1):
                if (x, y) in intersections:
                    line += '&'
                elif (x, y) in self.walls:
                    line += '#'
                elif (x, y) in self.keys:
                    line += 'k'
                elif (x, y) in self.doors:
                    line += 'D'
                else:
                    line += '.'
            print(line)

    def generate_lines(self):
        critical_points = self.get_splits()
        critical_points.update(self.keys)
        critical_points.add(self.cursor)
        for critical_point in critical_points:
            self.lines[critical_point] = self._generate_lines(critical_point, critical_points)

    def get_path_sides(self, path_criteria, final_criteria) -> {(int, int)}:
        result = set()
        for y in range(max(coord[1] for coord in self.walls)):
            for x in range(max(coord[0] for coord in self.walls)):
                path_count = 0
                if (x, y) not in self.walls:
                    for action in self.ACTIONS:
                        if path_criteria((x + action[0], y + action[1])):
                            path_count += 1
                    if final_criteria(path_count):
                        result.add((x, y))
        return result

    def get_splits(self) -> {(int, int)}:
        return self.get_path_sides(lambda coord: coord not in self.walls, lambda count: count > 2)

    def get_dead_ends(self) -> {(int, int)}:
        return self.get_path_sides(lambda coord: coord not in self.walls, lambda count: count == 1)

    def copy(self):
        return Maze(self.walls.copy(), self.keys.copy(), self.doors.copy(), self.cursor)


class Path:

    def __init__(self, maze: Maze, history: {Line}, start: (int, int), cursor: (int, int),
                 end: (int, int)):
        self.maze = maze
        self.history = history
        self.start = start
        self.cursor = cursor
        self.end = end

    def get_next(self) -> {'Path'}:
        result = set()

        for line in self.maze.lines[self.cursor]:
            if line not in self.history:
                history = self.history.copy()
                history.append(line)
                result.add(Path(self.maze, history, self.start, line.end, self.end))
        return result

    def get_dependencies(self):
        return {door for line in self.history for door in line.doors}

    def is_done(self) -> bool:
        return self.cursor == self.end

    def __len__(self):
        return sum(len(line) for line in self.history)

    def __str__(self):
        return f'start={self.start}, end={self.end}, cursor={self.cursor}, ' \
               f'history={",".join([str(line) for line in self.history])}'


class Solver:

    def __init__(self, maze: Maze, history: [Path], key_paths: {(int, int): {(int, int): Path}}):
        self.maze = maze
        self.history = history
        self.key_paths = key_paths

    def get_next(self) -> {'Solver'}:
        result = set()
        for reachable in self.get_reachable():
            next_maze = self.maze.copy()
            next_maze.obtain_key(reachable.end)
            history = self.history.copy()
            history.append(reachable)
            result.add(Solver(next_maze, history, self.key_paths))
        return result

    def get_reachable(self):
        result = set()
        for target in self.maze.keys:
            if len(self.key_paths[self.maze.cursor][target].get_dependencies().intersection(
                    {key for key in self.maze.doors})) == 0:
                result.add(self.key_paths[self.maze.cursor][target])
        return result

    def is_solved(self):
        return len(self.maze.keys) == 0

    def __len__(self):
        return sum({len(path) for path in self.history})

    def __str__(self):
        return ', '.join([str(len(line)) for line in self.history]) + " :: " + ', '.join(
            [str(line.start) for line in self.history])


def get_path(maze: Maze, start: (int, int), end: (int, int)) -> Path:
    paths: {int: {Path}} = {0: {Path(maze, [], start, start, end)}}
    best_path = None
    best_length = 0
    while len(paths) > 0 and (not best_length or best_length < min(paths)):
        length = min(paths)
        targets = paths[length]
        del paths[length]

        for target in targets:
            for next_target in target.get_next():
                next_length = len(next_target)
                if not next_target.is_done():
                    if next_length in paths:
                        paths[next_length].add(next_target)
                    else:
                        paths[next_length] = {next_target}
                else:
                    if not best_length or best_length > next_length:
                        best_length = next_length
                        best_path = next_target
    return best_path


def read_maze_from_file() -> Maze:
    maze: Maze = Maze()
    y = 0
    with open('input.txt') as file:
        for line in file.readlines():
            line = line.strip()
            for x in range(len(line)):
                if line[x] == '#':
                    maze.walls.add((x, y))
                elif line[x] == '@':
                    maze.cursor = (x, y)
                elif line[x].upper() != line[x].lower() == line[x]:
                    maze.keys[(x, y)] = line[x]
                elif line[x].lower() != line[x].upper() == line[x]:
                    maze.doors[(x, y)] = line[x]
            y += 1
    print(maze.doors)
    print(maze.keys)

    return maze


def get_key_paths(maze: Maze) -> {(int, int): {(int, int): Path}}:
    paths = {}
    i = 1
    for start_coord in maze.keys:
        if maze.cursor in paths:
            paths[maze.cursor][start_coord] = get_path(maze, maze.cursor, start_coord)
        else:
            paths[maze.cursor] = {start_coord: get_path(maze, maze.cursor, start_coord)}

        print(f'Calculated path {i}')
        i += 1
        for end_coord in maze.keys:
            if start_coord != end_coord:
                path = get_path(maze, start_coord, end_coord)

                if start_coord in paths:
                    paths[start_coord][end_coord] = path
                else:
                    paths[start_coord] = {end_coord: path}

    return paths


def shortest_path(maze: Maze) -> Solver:
    solvers: {int: {Solver}} = {0: {Solver(maze, [], get_key_paths(maze))}}
    best_length = 0
    best_route = 0

    while len(solvers) > 0 and (not best_length or best_length > min(solvers)):
        target_length = min(solvers)
        targets = solvers[target_length]
        del solvers[target_length]
        for target in targets:
            for next_target in target.get_next():
                target_length = len(next_target)
                if not next_target.is_solved():
                    if target_length not in solvers:
                        solvers[target_length] = {next_target}
                    else:
                        solvers[target_length].add(next_target)
                else:
                    if not best_length or target_length < best_length:
                        best_length = target_length
                        best_route = next_target

    return best_route


def part1():
    maze: Maze = read_maze_from_file()
    maze.generate_lines()
    # paths = get_key_paths(maze)
    path = shortest_path(maze)
    print(path)
    print(len(path))


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
