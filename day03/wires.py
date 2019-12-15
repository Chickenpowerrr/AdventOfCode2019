import re

NUMBER_PATTERN = re.compile('\\d+')


class Line:

    def __init__(self, start: (int, int), end: (int, int)):
        self._start = start
        self._end = end

    def covers(self, coord: (int, int)) -> bool:
        min_x = min(self._start[0], self._end[0])
        max_x = max(self._start[0], self._end[0])
        min_y = min(self._start[1], self._end[1])
        max_y = max(self._start[1], self._end[1])
        return min_x <= coord[0] <= max_x and min_y <= coord[1] <= max_y

    def intersections(self, line: 'Line') -> [(int, int)]:
        result = []
        if self.is_horizontal() != line.is_horizontal():
            if self.is_horizontal():
                critical: (int, int) = (line._start[0], self._start[1])
                if self.covers(critical) and line.covers(critical):
                    result.append(critical)
            else:
                critical: (int, int) = (self._start[0], line._start[1])
                if self.covers(critical) and line.covers(critical):
                    result.append(critical)
        else:
            if self.is_horizontal():
                if self._start[1] == line._start[1]:
                    min_x = min(line._start[0], line._end[0])
                    max_x = max(line._start[0], line._end[0])
                    for i in range(min(self._start[0], self._end[0]),
                                   max(self._start[0], self._end[0])):
                        if min_x <= i <= max_x:
                            result.append((i, self._start[1]))
            else:
                if self._start[0] == line._start[0]:
                    min_y = min(line._start[1], line._end[1])
                    max_y = max(line._start[1], line._end[1])
                    for i in range(min(self._start[1], self._end[1]),
                                   max(self._start[1], self._end[1])):
                        if min_y <= i <= max_y:
                            result.append((self._start[0], i))
        return result

    def is_horizontal(self) -> bool:
        return self._start[1] == self._end[1]

    def __len__(self):
        return abs(self._end[0] - self._start[0]) + abs(self._end[1] - self._start[1])


def move_direction(cursor: (int, int), path: [Line], function) -> (int, int):
    next_cursor = function(cursor)
    path.append(Line(cursor, next_cursor))
    return next_cursor


def move(instruction: str, cursor: (int, int), path: [Line]) -> (int, int):
    distance: int = int(NUMBER_PATTERN.findall(instruction)[0])
    if instruction.startswith('U'):
        return move_direction(cursor, path, lambda c: (c[0], c[1] + distance))
    elif instruction.startswith('D'):
        return move_direction(cursor, path, lambda c: (c[0], c[1] - distance))
    elif instruction.startswith('R'):
        return move_direction(cursor, path, lambda c: (c[0] + distance, c[1]))
    else:
        return move_direction(cursor, path, lambda c: (c[0] - distance, c[1]))


def execute(instructions: [str]) -> [Line]:
    path: [Line] = []
    cursor = (0, 0)
    for instruction in instructions:
        cursor = move(instruction, cursor, path)
    return path


def split(instruction: str) -> [str]:
    return instruction.replace('\n', '').split(',')


def intersection(first: [Line], second: [Line]) -> [(int, int, int)]:
    intersections: [(int, int, int)] = []
    first_length = 0
    for line1 in first:
        second_length = 0
        for line2 in second:
            temp = line1.intersections(line2)
            if len(temp) > 0:
                intersections.extend([(coord[0], coord[1], (first_length + second_length + distance(
                    coord, line1._start) + distance(coord, line2._start))) for coord in temp])
            second_length += len(line2)
        first_length += len(line1)
    return intersections


def distance(first: (int, int), second: (int, int)):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


with open('input.txt') as file:
    first_instructions: str = file.readline()
    second_instructions: str = file.readline()

    intersections = intersection(execute(split(first_instructions)),
                                 execute(split(second_instructions)))
    intersections.remove((0, 0, 0))
    print(min([abs(coord[0]) + abs(coord[1]) for coord in intersections]))
    print(min([coord[2] for coord in intersections]))
