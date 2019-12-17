import re
from enum import Enum

from day17.input import INSTRUCTIONS
from day17.vision import Board, get_board


class Direction(Enum):
    UP = (ord('^'), 0)
    RIGHT = (ord('>'), 90)
    DOWN = (ord('v'), 180)
    LEFT = (ord('<'), 270)

    def is_opposite(self, other: 'Direction'):
        return abs(self.value[1] - other.value[1]) == 180

    def get_difference(self, new_direction: 'Direction') -> int:
        if new_direction.value[1] - self.value[1] == 90:
            return ord('R')
        else:
            return ord('L')


class Link:

    def __init__(self, start: (int, int), previous: (int, int) = None, moves: [int] = None,
                 cursor: (int, int) = None, direction: Direction = None,
                 start_direction: Direction = None, editing_length=False):
        self.start = start
        self.moves = moves if moves else []
        self.start_direction = start_direction
        self.cursor = cursor if cursor else start
        self.previous = previous if previous else cursor
        self.direction = direction
        self.editing_length = editing_length

    def attempt_perform_move(self, delta_x: int, delta_y: int, filled, target_color) -> bool:
        target = self.cursor[0] + delta_x, self.cursor[1] + delta_y

        if target != self.previous and target in filled and filled[target] == target_color:
            next_direction = get_angle(self.previous, target)
            if not self.start_direction:
                self.start_direction = self.direction = next_direction
            elif next_direction != self.direction:
                self.editing_length = False
                self.moves.append(self.direction.get_difference(next_direction))
                self.direction = next_direction

            if self.editing_length:
                self.moves[-1] += 1
            else:
                self.editing_length = True
                self.moves.append(1)

            self.previous = self.cursor
            self.cursor = target

            return True
        else:
            return False

    def copy(self):
        return Link(self.start, self.previous, self.moves.copy(), self.cursor, self.direction,
                    self.start_direction, self.editing_length)


class Path:

    def __init__(self, history: [Link], to_cover: {(int, int): {Link}}):
        self.history = history
        self.to_cover = to_cover

    def get_next(self) -> {'Path'}:
        result = set()
        cursor = self.history[-1].cursor
        # Cursor = Current position
        if cursor in self.to_cover:
            for link in self.to_cover[cursor]:
                history = self.history.copy()
                history.append(link)
                to_cover = self.to_cover.copy()

                if len(to_cover[cursor]) > 1:
                    temp = to_cover[cursor].copy()
                    temp.remove(link)
                    to_cover[cursor] = temp
                else:
                    del to_cover[cursor]

                if link.start in to_cover:
                    counter_links = to_cover[link.start].copy()
                    for counter_link in counter_links.copy():
                        if counter_link.cursor == cursor:
                            counter_links.remove(counter_link)
                    to_cover[link.start] = counter_links

                    if len(to_cover[link.start]) == 0:
                        del to_cover[link.start]

                result.add(Path(history, to_cover))
        return result

    def get_instructions(self, start_direction: Direction) -> [int]:
        result: [int] = []
        previous_link = None
        for link in self.history:
            previous_direction = previous_link.start_direction if previous_link else start_direction
            if previous_direction != link.start_direction:
                if not previous_direction.is_opposite(link.start_direction):
                    result.append(ord('R'))
                    result.append(ord('R'))
                else:
                    result.append(previous_direction.get_difference(link.start_direction))

                result.extend(link.moves)
                previous_link = link
        return result


def get_end_point(filled) -> (int, int):
    for pos in filled:
        up = pos[0], pos[1] + 1
        down = pos[0], pos[1] - 1
        right = pos[0] + 1, pos[1]
        left = pos[0] - 1, pos[1]

        if (up not in filled or filled[up] != ord('.')) and \
                (down not in filled or filled[down] != ord('.')) and \
                (right not in filled or filled[right] != ord('.')) and \
                (left not in filled or filled[left] != ord('.')):
            return pos


def get_links(point: (int, int), critical_points: {(int, int)}, filled,
              target_color) -> {(int, int)}:
    targets: {Link} = set()
    targets.add(Link(point))
    found: {Link} = set()

    while len(targets) > 0:
        temp_targets = targets.copy()
        targets = set()
        for target in temp_targets:
            if len(target.moves) == 0 or target.cursor not in critical_points:
                up = target.copy()
                down = target.copy()
                right = target.copy()
                left = target.copy()

                if up.attempt_perform_move(0, 1, filled, target_color):
                    targets.add(up)
                if down.attempt_perform_move(0, -1, filled, target_color):
                    targets.add(down)
                if right.attempt_perform_move(1, 0, filled, target_color):
                    targets.add(right)
                if left.attempt_perform_move(-1, 0, filled, target_color):
                    targets.add(left)
            else:
                found.add(target)
    return found


def get_all_links(critical_points: {(int, int)}, filled, target_color):
    links: {(int, int): {Link}} = {}
    for critical_point in critical_points:
        for link in get_links(critical_point, critical_points, filled, target_color):
            if critical_point not in links:
                links[critical_point] = set()
            links[critical_point].add(link)
    return links


def get_all_paths(critical_points, filled, start_point):
    all_links = get_all_links(critical_points, filled, ord('#'))

    start_links = all_links.copy()
    start_history = [list(start_links[start_point])[0]]
    del start_links[start_point]

    paths = set()
    paths.add(Path(start_history, start_links))
    result = set()

    while len(paths) > 0:
        print(len(paths))
        temp_paths = paths.copy()
        paths = set()
        for path in temp_paths:
            if len(path.to_cover) > 0:
                paths.update(path.get_next())
            else:
                result.add(path)

    return result


def get_angle(original_location: (int, int), new_location: (int, int)) -> Direction:
    if original_location[0] < new_location[0]:
        return Direction.RIGHT
    elif original_location[0] > new_location[0]:
        return Direction.LEFT
    elif original_location[1] < new_location[1]:
        return Direction.UP
    else:
        return Direction.DOWN


def pattern_count(pattern, iterable):
    iterable = ','.join(map(str, iterable))
    pattern = ','.join(map(str, pattern))
    return len(re.findall(pattern, iterable))


def best_split(instructions: [int]):
    best_efficiency = 0

    for i in range(len(instructions) - 3):
        for j in range(3, 10):
            if i + j + 1 < len(instructions):
                efficiency = (pattern_count(instructions[i:(i + j + 1)], instructions) - 1) * j
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
    return best_efficiency


def part2():
    board: Board = get_board()
    instructions: [int] = INSTRUCTIONS.copy()
    critical_points: {(int, int)} = board.intersections(35)
    start_point: (int, int) = [pos for pos in board.filled if board.filled[pos] == ord('^')][0]
    end_point: (int, int) = get_end_point(board.filled)

    critical_points.add(start_point)
    critical_points.add(end_point)

    paths = get_all_paths(critical_points, board.filled, start_point)
    print(len(paths))
    print({path.history[-1].cursor for path in paths})
    print([best_split(path.get_instructions(Direction.UP)) for path in paths])

    best_total = 0
    best_before = 0
    for path in paths:
        path_instructions = path.get_instructions(Direction.UP)
        total = len(path_instructions) - best_split(path_instructions)

        if not best_before or len(path_instructions) < best_before:
            best_before = len(path_instructions)

        if not best_total or total < best_total:
            best_total = total

    print(f'Best total: {best_total}')
    print(f'Best before: {best_before}')


part2()
