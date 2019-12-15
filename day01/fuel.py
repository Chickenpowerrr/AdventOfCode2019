def calculate_part_fuel(mass: int) -> int:
    partial_fuel: int = mass // 3 - 2
    return partial_fuel + calculate_part_fuel(partial_fuel) if partial_fuel > 0 else 0


def get_input():
    total_masses = []
    with open('input.txt') as file:
        line = file.readline()
        while line:
            total_masses.append(int(line))
            line = file.readline()
    return total_masses


def part1():
    fuel = sum([mass // 3 - 2 for mass in get_input()])
    print(f'Fuel sum: {fuel}')


def part2():
    fuel = sum([calculate_part_fuel(mass) for mass in get_input()])
    print(f'Total fuel: {fuel}')


if __name__ == '__main__':
    part1()
    part2()
