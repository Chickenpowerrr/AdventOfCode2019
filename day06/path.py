class Path:

    def __init__(self, passes: [str]):
        self.passes = passes

    def __contains__(self, item):
        return item in self.passes

    def __len__(self):
        return len(self.passes)

    def clone(self):
        return Path(self.passes.copy())


def calculate_route(connections: {str: [str]}, start: str, end: str):
    paths: {int, [Path]} = {0: [Path([start])]}
    shortest_path: Path = None

    while not shortest_path or min(paths) < len(shortest_path):
        targets: [Path] = paths[min(paths)]
        del paths[min(paths)]

        for target in targets:
            if target.passes[-1] != end:
                for next_node in connections[target.passes[-1]]:
                    if next_node not in target:
                        cursor = target.clone()
                        cursor.passes.append(next_node)
                        if len(cursor) not in paths:
                            paths[len(cursor)] = [cursor]
                        else:
                            paths[len(cursor)].append(cursor)
            else:
                if not shortest_path or len(shortest_path) > len(target):
                    shortest_path = target

    return len(shortest_path)
