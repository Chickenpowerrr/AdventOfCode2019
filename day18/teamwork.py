from day18.maze import Line

ACTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class Path:

    def __init__(self, history: {Line}, start: (int, int), cursor: (int, int),
                 end: (int, int), lines: {(int, int): {Line}}):
        self.history = history
        self.start = start
        self.cursor = cursor
        self.end = end
        self.lines = lines

    def get_next(self) -> {'Path'}:
        result = set()

        for line in self.lines[self.cursor]:
            if line not in self.history:
                history = self.history.copy()
                history.append(line)
                result.add(Path(history, self.start, line.end, self.end, self.lines))
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


class Maze:

    def __init__(self, cursors, doors, keys, walls):
        self.cursors = cursors
        self.doors = doors
        self.keys = keys
        self.walls = walls

    def obtain_key(self, location: (int, int)):
        name = self.keys[location].upper()
        del self.keys[location]
        for door in self.doors.copy():
            if self.doors[door] == name:
                del self.doors[door]

    def copy(self):
        return Maze(self.cursors.copy(), self.doors.copy(), self.keys.copy(), self.walls.copy())


class Solver:

    def __init__(self, maze: Maze, history: [(Path, int)],
                 key_paths: {(int, int): {(int, int): Path}}):
        self.maze = maze
        self.history = history
        self.key_paths = key_paths

    def get_next(self) -> {'Solver'}:
        result = set()
        for reachable in self.get_reachable():
            next_maze = self.maze.copy()
            location = reachable[0].end

            next_maze.obtain_key(location)
            next_maze.cursors[next_maze.cursors.index(reachable[1])] = location

            history = self.history.copy()
            history.append((reachable[0], self.maze.cursors.index(reachable[1])))
            result.add(Solver(next_maze, history, self.key_paths))
        return result

    def get_reachable(self):
        result = set()
        for cursor in self.maze.cursors:
            for target in self.maze.keys:
                if target in self.key_paths[cursor] and \
                        len(self.key_paths[cursor][target].get_dependencies().intersection(
                            {key for key in self.maze.doors})) == 0:
                    result.add((self.key_paths[cursor][target], cursor))
        return result

    def is_solved(self):
        return len(self.maze.keys) == 0

    def get_covered(self) -> {(((int, int), ...), ((int, int), ...)): (int, [(int, int)])}:
        covered = {}
        history_places = [line[0].end for line in self.history]
        cursors = [None for _ in range(4)]

        for i in range(len(history_places)):
            cursors = cursors.copy()
            cursors[self.history[i][1]] = history_places[i]
            cursor_history = history_places[:i + 1].copy()
            for cursor in cursors:
                if cursor:
                    cursor_history.remove(cursor)

            covered[(tuple(sorted(cursor_history)), tuple(cursors))] = \
                (sum([len(entry[0]) for entry in self.history[:i + 1]]), history_places[:i + 1])
        return covered

    def __len__(self):
        return sum([len(entry[0]) for entry in self.history])

    def __str__(self):
        return '->'.join([str(keys[line[0].end]) for line in self.history])


def get_path(start: (int, int), end: (int, int), lines: {(int, int): {Line}}) -> Path:
    paths: {int: {Path}} = {0: {Path([], start, start, end, lines)}}
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


def get_key_paths(keys: {(int, int)},
                  lines: {(int, int): {Line}}) -> {(int, int): {(int, int): Path}}:
    paths = {}
    i = 1
    for start in keys:
        i += 1
        for end in keys:
            if start != end:
                path = get_path(start, end, lines)
                if path:
                    if start in paths:
                        paths[start][end] = path
                    else:
                        paths[start] = {end: path}

    return paths


def get_lines(start: (int, int), characters: {(int, int): str},
              critical_points: {(int, int)}) -> [Line]:
    targets: [((int, int), (int, int), int, {(int, int)})] = [(start, start, 0, set())]
    result = []

    while len(targets) > 0:
        temp_targets = targets.copy()
        targets = []

        for target in temp_targets:
            for action in ACTIONS:
                next_target = target[0][0] + action[0], target[0][1] + action[1]
                if next_target in characters and characters[next_target] != '#' \
                        and next_target != target[1]:
                    if next_target not in critical_points:
                        character = characters[next_target]
                        history = target[3].copy()
                        if character.isalpha():
                            history.add(next_target)
                        targets.append((next_target, target[0], target[2] + 1, history))
                    else:
                        result.append(Line(target[2] + 1, start, next_target, target[3]))
    return result


def get_all_lines(characters: {(int, int): str},
                  critical_points: {(int, int)}) -> {(int, int): [Line]}:
    result = {}
    for location in critical_points:
        result[location] = get_lines(location, characters, critical_points)
    return result


def get_start(characters: {(int, int): str}) -> {(int, int)}:
    return [location for location in characters if characters[location] == '@']


def get_keys(characters: {(int, int): str}) -> {(int, int): str}:
    keys = {}
    for location in characters:
        character = characters[location]
        if character.isalpha() and character.islower():
            keys[location] = character
    return keys


def get_doors(characters: {(int, int): str}) -> {(int, int): str}:
    keys = {}
    for location in characters:
        character = characters[location]
        if character.isalpha() and character.isupper():
            keys[location] = character
    return keys


def get_walls(characters: {(int, int): str}) -> {(int, int)}:
    return [location for location in characters if characters[location] == '#']


def get_intersections(characters: {(int, int): str}) -> {(int, int)}:
    intersections = set()
    for location in characters:
        count = 0

        if characters[location] != '#':
            for action in ACTIONS:
                cursor = location[0] + action[0], location[1] + action[1]
                if cursor in characters and characters[cursor] != '#':
                    count += 1
            if count > 2:
                intersections.add(location)
    return intersections


def read_file() -> {(int, int): str}:
    characters: {(int, int): str} = {}
    with open('input.txt') as file:
        y = 0
        for line in file.readlines():
            line = line.strip()
            x = 0
            for character in line:
                if (x, y) not in characters:
                    if character != '@':
                        characters[(x, y)] = character
                    else:
                        characters[(x, y)] = '#'

                        characters[(x - 1, y - 1)] = '@'
                        characters[(x + 1, y - 1)] = '@'
                        characters[(x - 1, y + 1)] = '@'
                        characters[(x + 1, y + 1)] = '@'

                        characters[(x - 1, y)] = '#'
                        characters[(x + 1, y)] = '#'
                        characters[(x, y - 1)] = '#'
                        characters[(x, y + 1)] = '#'
                x += 1
            y += 1
    return characters


def render(characters: {(int, int): str}):
    intersections = get_intersections(characters)
    for y in range(max(coord[1] for coord in characters) + 1):
        line = ''
        for x in range(max(coord[0] for coord in characters) + 1):
            if (x, y) in intersections:
                line += '&'
            else:
                line += characters[(x, y)]
        print(line)


def shortest_path(maze: Maze, targets: {(int, int)}, lines: {(int, int): {Line}}):
    solvers: {int: {Solver}} = {0: {Solver(maze, [], get_key_paths(targets, lines))}}
    best_paths: {(((int, int), ...), ((int, int), ...)): (int, [(int, int)])} = {}
    best_length = 0
    best_route = 0

    while len(solvers) > 0 and (not best_length or best_length > min(solvers)):
        # print(sum([len(solvers[length]) for length in solvers]))
        target_length = min(solvers)
        targets = solvers[target_length]
        del solvers[target_length]
        for target in targets:
            # print(target)
            for next_target in target.get_next():
                target_length = len(next_target)
                if not next_target.is_solved():
                    covered = next_target.get_covered()
                    better_alternative = False
                    for piece in covered:
                        if piece in best_paths:
                            if best_paths[piece][0] < covered[piece][0]:
                                better_alternative = True
                                break
                            elif best_paths[piece][0] > covered[piece][0]:
                                best_paths[piece] = covered[piece]
                            else:
                                if best_paths[piece][1] != covered[piece][1]:
                                    better_alternative = True
                                    break
                        else:
                            best_paths[piece] = covered[piece]

                    if not better_alternative:
                        if target_length not in solvers:
                            solvers[target_length] = {next_target}
                        else:
                            solvers[target_length].add(next_target)
                else:
                    if not best_length or target_length < best_length:
                        best_length = target_length
                        best_route = next_target

    return best_route


keys = None


def part2():
    global keys

    characters = read_file()
    intersections = get_intersections(characters)
    keys = get_keys(characters)
    start = get_start(characters)

    critical_points = intersections.copy()
    critical_points.update(keys)
    critical_points.update(start)

    lines = get_all_lines(characters, critical_points)
    targets = {location for location in keys}
    targets.update(start)

    path = shortest_path(Maze(start, get_doors(characters), get_keys(characters),
                              get_walls(characters)), targets, lines)
    print(path)
    print(len(path))


if __name__ == '__main__':
    part2()
