ACTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}


class Portal:

    def __init__(self, name: str, start: (int, int), end: (int, int), outside: bool):
        self.name = name
        self.start = start
        self.end = end
        self.outside = outside

    def __str__(self):
        return f'<name={self.name}, start={self.start}, end={self.end}>'


class Line:

    def __init__(self, start: Portal, end: Portal, length: int):
        self.start = start
        self.end = end
        self.length = length

    def __len__(self):
        return self.length

    def __eq__(self, other):
        return isinstance(other, Line) and (self.start == other.end or self.start == other.start) \
               and (self.end == other.end or self.end == other.start)

    def __str__(self):
        return f'<from={self.start}, to={self.end}, len={self.length}>'


class Path:

    def __init__(self, start: (int, int), end: (int, int), cursor: (int, int) = None,
                 history: [Line] = None, visited: {((int, int), bool)} = None, level: int = 0):
        self.start = start
        self.end = end
        self.level = level
        self.cursor = cursor if cursor else start
        self.history = history if history else []
        self.visited = visited if visited else {start}

    def copy(self):
        return Path(self.start, self.end, self.cursor, self.history.copy(), self.visited,
                    self.level)

    def finished(self) -> bool:
        return self.cursor == self.end

    def __len__(self):
        return sum(map(len, self.history))

    def __str__(self):
        return f"level={self.level}, <history=<AA->{'->'.join([line.end.name for line in self.history])}>>"


def read_map():
    characters: {(int, int): str} = {}
    with open('input.txt') as file:
        y = 0
        for line in file.readlines():
            line = line.replace('\n', '')
            x = 0
            for character in line:
                characters[(x, y)] = character
                x += 1
            y += 1
    return characters


def get_lines(start: (int, int), characters: {(int, int): str},
              portals: {(int, int): {Portal}}) -> {(int, int): {Line}}:
    history = {start}
    targets: ((int, int), int) = {(start, 0)}
    result = {}

    while len(targets) > 0:
        temp_targets = targets.copy()
        targets = set()

        for target in temp_targets:
            for action in ACTIONS:
                cursor = target[0][0] + action[0], target[0][1] + action[1]
                if cursor in characters and characters[cursor] == '.' and cursor not in history:
                    history.add(cursor)
                    if cursor not in portals:
                        targets.add((cursor, target[1] + 1))
                    else:
                        line = Line(portals[start], portals[cursor], target[1] + (
                            2 if portals[cursor].start != portals[cursor].end else 1))
                        if start not in result:
                            result[start] = [line]
                        else:
                            result[start].append(line)
    return result


def get_all_lines(characters: {(int, int): str}, portals: {(int, int): {Portal}}) \
        -> {(int, int): {Line}}:
    result = {}
    for portal in portals:
        result.update(get_lines(portal, characters, portals))
    return result


def get_portals(characters: {(int, int): str}) -> {(int, int): Portal}:
    portal_locations: {str: {(int, int)}} = {}
    min_portal_x = 2
    max_portal_x = max(location[0] for location in characters) - 2
    min_portal_y = 2
    max_portal_y = max(location[1] for location in characters) - 2

    for location in characters:
        character = characters[location]
        if character.isalpha():
            portal_location = None
            joined_character = None
            for action in ACTIONS:
                cursor = location[0] + action[0], location[1] + action[1]
                if cursor in characters:
                    other_character = characters[cursor]
                    if other_character == '.':
                        portal_location = cursor
                    elif other_character.isalpha():
                        if action == (1, 0) or action == (0, 1):
                            joined_character = character
                            character = other_character
                        else:
                            joined_character = other_character

            if joined_character and portal_location:
                name = joined_character + character
                if name in portal_locations:
                    portal_locations[name].append(portal_location)
                else:
                    portal_locations[name] = [portal_location]

    result = {}

    for portal_name in portal_locations:
        start = portal_locations[portal_name][0]
        end = portal_locations[portal_name][1] if len(portal_locations[portal_name]) > 1 else start

        result[start] = Portal(portal_name, start, end,
                               start[0] == min_portal_x
                               or start[0] == max_portal_x
                               or start[1] == min_portal_y
                               or start[1] == max_portal_y)
        if end:
            result[end] = Portal(portal_name, end, start,
                                 end[0] == min_portal_x
                                 or end[0] == max_portal_x
                                 or end[1] == min_portal_y
                                 or end[1] == max_portal_y)
    return result


def get_shortest_path(start: (int, int), end: (int, int), lines: {(int, int): {Line}}):
    considering: {int, {Path}} = {0: {Path(start, end)}}

    best_length = 0
    best_route = None

    while len(considering) > 0 and (not best_length or best_length > min(considering)):
        target_length = min(considering)
        targets = considering[target_length]
        del considering[target_length]

        for target in targets:
            for next_line in lines[target.cursor]:
                if next_line.end not in target.visited:
                    next_path = target.copy()
                    next_path.history.append(next_line)
                    next_path.cursor = next_line.end.end
                    next_path.visited.add(next_path.cursor)

                    next_length = len(next_path)
                    if not next_path.finished():
                        if next_length not in considering:
                            considering[next_length] = {next_path}
                        else:
                            considering[next_length].add(next_path)
                    else:
                        if not best_length or best_length > next_length:
                            best_length = next_length
                            best_route = next_path

    return best_route


def get_shortest_recursive_path(start: (int, int), end: (int, int), lines: {(int, int): {Line}}):
    considering: {int, {Path}} = {0: {Path(start, end)}}

    best_length = 0
    best_route = None

    while len(considering) > 0 and (not best_length or best_length > min(considering)):
        target_length = min(considering)
        targets = considering[target_length]
        del considering[target_length]

        for target in targets:
            for next_line in lines[target.cursor]:
                if len(target.history) == 0 \
                        or next_line != target.history[-1] \
                        and next_line.end.end != start:
                    next_path = target.copy()

                    next_path.history.append(next_line)
                    next_path.cursor = next_line.end.end
                    next_path.visited.add(next_path.cursor)

                    next_length = len(next_path)
                    if not next_path.finished() and next_path.level >= 0:
                        if next_line.end.outside:
                            next_path.level -= 1
                        else:
                            next_path.level += 1

                        if next_length not in considering:
                            considering[next_length] = {next_path}
                        else:
                            considering[next_length].add(next_path)
                    else:
                        if next_path.level == 0 and (
                                not best_length or best_length > next_length):
                            best_length = next_length
                            best_route = next_path

    return best_route


def part1():
    characters = read_map()
    portals = get_portals(characters)
    start_portal = [portals[location] for location in portals if portals[location].name == 'AA'][0]
    end_portal = [portals[location] for location in portals if portals[location].name == 'ZZ'][0]
    lines = get_all_lines(characters, portals)
    path = get_shortest_path(start_portal.start, end_portal.start, lines)
    print(f'Shortest route from AA towards ZZ: {len(path)}')


def part2():
    characters = read_map()
    portals = get_portals(characters)
    start_portal = [portals[location] for location in portals if portals[location].name == 'AA'][0]
    end_portal = [portals[location] for location in portals if portals[location].name == 'ZZ'][0]
    lines = get_all_lines(characters, portals)
    path = get_shortest_recursive_path(start_portal.start, end_portal.start, lines)
    print(f'Shortest recursive route from AA towards ZZ: {len(path)}')


if __name__ == '__main__':
    part1()
    part2()
