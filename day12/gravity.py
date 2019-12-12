import math


def calculate_gravity(old_velocity: (int, int, int), target: (int, int, int),
                      relative_to: {((int, int, int), (int, int, int))}) -> (int, int, int):
    delta = [0, 0, 0]
    for relative in relative_to:
        for i in range(3):
            delta[i] += 1 if target[i] < relative[0][i] else -1 if target[i] > relative[0][i] else 0

    return old_velocity[0] + delta[0], old_velocity[1] + delta[1], old_velocity[2] + delta[2]


def apply_velocity(velocity: (int, int, int), old: ((int, int, int), (int, int, int))):
    return (old[0][0] + velocity[0], old[0][1] + velocity[1], old[0][2] + velocity[2]), velocity


def potential_energy(obj: ((int, int, int), (int, int, int))):
    return abs(obj[0][0]) + abs(obj[0][1]) + abs(obj[0][2])


def kinetic_energy(obj: ((int, int, int), (int, int, int))):
    return abs(obj[1][0]) + abs(obj[1][1]) + abs(obj[1][2])


def energy(obj: ((int, int, int), (int, int, int))):
    return potential_energy(obj) * kinetic_energy(obj)


def part1(objects):
    for _ in range(1000):
        temp = objects.copy()
        for obj in temp:
            objects.remove(obj)
            objects.append(apply_velocity(calculate_gravity(obj[1], obj[0], temp), obj))

    print(f'State: {objects}')
    print(f'Energy: {sum({energy(obj) for obj in objects})}')


def get_repeat(index: int, objects):
    history = set()

    while True:
        temp = objects.copy()
        for obj in temp:
            objects.remove(obj)
            objects.append(apply_velocity(calculate_gravity(obj[1], obj[0], temp), obj))

        target = ((objects[0][0][index], objects[1][0][index],
                   objects[2][0][index], objects[3][0][index]),
                  (objects[0][1][index], objects[1][1][index],
                   objects[2][1][index], objects[3][1][index]))

        if target not in history:
            history.add(target)
        else:
            break

    return len(history)


def get_target(x, y, z):
    i = 1
    while True:
        target = x * i
        if (target / y).is_integer() and (target / z).is_integer():
            return target
        i += 1


def lcm(numbers: [int]):
    result = numbers[0]
    for i in numbers[1:]:
        result = result * i // math.gcd(result, i)
    return result


def part2(objects):
    x = get_repeat(0, objects.copy())
    y = get_repeat(1, objects.copy())
    z = get_repeat(2, objects.copy())
    print(f'Repeats: X={x}, Y={y}, Z={z}')
    print(f'LCM: {lcm([x, y, z])}')


if __name__ == '__main__':
    with open('input.txt') as file:
        line = file.readline()
        objects = []
        while line:
            parts = line.replace('\n', '').replace('>', '').split(',')
            objects.append(((int(parts[0].split('=')[1]), int(parts[1].split('=')[1]),
                             int(parts[2].split('=')[1])), (0, 0, 0)))
            line = file.readline()
    part1(objects.copy())
    part2(objects.copy())
