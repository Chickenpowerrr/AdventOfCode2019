import math


class Reaction:

    def __init__(self, name: str, quantity: int, costs: {str: int}):
        self.name = name
        self.quantity = quantity
        self.costs = costs

    def __str__(self):
        return f'{self.quantity} {self.name} {self.costs}'


def get_reactions() -> {str: Reaction}:
    result = {}
    with open('input.txt') as file:
        line = file.readline()
        while line:
            parts = line.replace('\n', '').split(' => ')
            inputs = parts[0].split(', ')
            costs = {}
            for val in inputs:
                part = val.split(' ')
                costs[part[1]] = int(part[0])
            part = parts[1].split(' ')
            result[part[1]] = Reaction(part[1], int(part[0]), costs)
            line = file.readline()
    return result


def required_materials(quantity: int, name: str, values: {str: int}, spare: {str: int},
                       reactions: {str: Reaction}):
    if name in reactions:
        if name in values:
            values[name] += quantity
        else:
            values[name] = quantity

        reaction = reactions[name]
        left = spare[name] if name in spare else 0
        if left >= quantity:
            spare[name] -= quantity
            quantity = 0
        elif left > 0:
            del spare[name]
            quantity -= left

        produce_times = math.ceil(quantity / reaction.quantity)
        if produce_times > 0:
            produced = produce_times * reaction.quantity
            if produced > quantity:
                if name in spare:
                    spare[name] += produced - quantity
                else:
                    spare[name] = produced - quantity
            for required in reaction.costs:
                required_materials(produce_times * reaction.costs[required], required, values,
                                   spare, reactions)
    else:
        if name in values:
            values[name] += quantity
        else:
            values[name] = quantity


def part1():
    values = {}
    left = {}
    required_materials(1, 'FUEL', values, left, get_reactions())

    print(values)
    print(left)
    print(f'Required for 1 fuel: {values["ORE"]}')


def part2(collected):
    values = {}
    required_materials(1, 'FUEL', values, {}, get_reactions())
    base = collected // values['ORE']
    for i in range(base + 700_000, base + 750_000):
        values = {}
        required_materials(i, 'FUEL', values, {}, get_reactions())
        if values['ORE'] > collected:
            return i - 1


if __name__ == '__main__':
    part1()
    print(f'Can collect: {part2(1000000000000)}')
