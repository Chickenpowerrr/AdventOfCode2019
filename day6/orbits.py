from day6.path import calculate_route


class Orbit:

    def __init__(self, name: str, orbits: ['Orbit']):
        self.name = name
        self.orbits = orbits


orbits: {str: Orbit} = {}
existing_orbits: {str} = set()
dependencies: {str: str} = {}
connections: {str: [str]} = {}

with open('input.txt') as file:
    for line in file.readlines():
        parts = line.replace('\n', '').split(')')
        dependencies[parts[1]] = parts[0]
        existing_orbits.add(parts[0])
        existing_orbits.add(parts[1])

        if parts[0] not in connections:
            connections[parts[0]] = [parts[1]]
        else:
            connections[parts[0]].append(parts[1])

        if parts[1] not in connections:
            connections[parts[1]] = [parts[0]]
        else:
            connections[parts[1]].append(parts[0])

    while len(existing_orbits) > 0:
        for orbit in existing_orbits.copy():
            if orbit not in dependencies:
                existing_orbits.remove(orbit)
                orbits[orbit] = Orbit(orbit, [])
            elif dependencies[orbit] in orbits:
                existing_orbits.remove(orbit)
                target = Orbit(orbit, orbits[dependencies[orbit]].orbits.copy())
                target.orbits.append(orbits[dependencies[orbit]])
                orbits[orbit] = target

print(sum([len(orbits[name].orbits) for name in orbits]))
print(calculate_route(connections, 'YOU', 'SAN') - 3)
