import math


def get_y(first: (int, int), second: (int, int), x: int):
    return first[1] + (second[1] - first[1]) / (second[0] - first[0]) * (x - first[0])


class Asteroid:

    def __init__(self, location: (int, int)):
        self.location = location

    def can_spot(self, other: (int, int), asteroids: {(int, int)}):
        if self.location[0] == other[0]:
            for y in range(min(other[1] + 1, self.location[1] + 1),
                           max(other[1], self.location[1])):
                if (self.location[0], y) in asteroids:
                    return False
            return True
        else:
            for x in range(min(other[0] + 1, self.location[0] + 1),
                           max(other[0], self.location[0])):
                y = get_y(self.location, other, x)
                if y.is_integer() and (x, y) in asteroids:
                    return False
            return True

    def get_sight(self, asteroids: {(int, int)}):
        return len([asteroid for asteroid in asteroids if self.can_spot(asteroid, asteroids)]) - 1

    def get_angle(self, location: (int, int)) -> float:
        base = math.atan2(location[0] - self.location[0], location[1] - self.location[1])
        return base if base > 0 else 2 * math.pi + base

    def distance(self, location: (int, int)):
        return math.sqrt(
            (self.location[0] - location[0]) ** 2 + (self.location[1] - location[1]) ** 2)


def read(line: str, y: int) -> {(int, int)}:
    result = set()
    for x in range(0, len(line)):
        if line[x] == '#':
            result.add((x, y))
    return result


with open('input.txt') as file:
    line = file.readline()
    locations = set()
    y = 0
    while line:
        line.replace('\n', '')
        locations.update(read(line, y))
        line = file.readline()
        y += 1

    max_sight = None
    max_location = None
    for loc in locations:
        sight = Asteroid(loc).get_sight(locations)
        if max_sight is None or sight > max_sight:
            max_sight = sight
            max_location = loc

    print(f'Max sight: {max_sight} for {max_location}')

    locations.remove(max_location)
    targets = sorted([Asteroid(loc) for loc in locations],
                     key=lambda asteroid: (-asteroid.get_angle(max_location),
                                           asteroid.distance(max_location)))

    vaporized = 0
    while len(targets) > 0:
        temp = locations.copy()
        for target in targets.copy():
            if target.can_spot(max_location, temp):
                vaporized += 1
                if vaporized == 200:
                    print(f'{vaporized}. {target.location}')
                    print(f'Bet: {100 * target.location[0] + target.location[1]}')
                targets.remove(target)
                locations.remove(target.location)
