def calculate_fuel(load: [int]) -> int:
    return sum([calculate_part_fuel(mass) for mass in load])


def calculate_part_fuel(mass: int) -> int:
    partial_fuel: int = int(mass / 3) - 2
    if partial_fuel > 0:
        return partial_fuel + calculate_part_fuel(partial_fuel)
    else:
        return 0


with open('input.txt') as file:
    total_masses = []
    line = file.readline()
    while line:
        total_masses.append(int(line))
        line = file.readline()
    print(calculate_fuel(total_masses))
