from day18.new import Maze, read_maze_from_file


class MazeWalker:
    ACTIONS = {(1, 0), (0, 1), (-1, 0), (0, -1)}

    def __init__(self, maze: Maze, moves: int = 0, found_keys: {(str, ...): int} = None,
                 last_found: (str, ...) = (), session_locations=None):
        self.maze = maze
        self.moves = moves
        self.last_found = last_found
        self.found_keys = found_keys if found_keys else {}
        self.session_locations = session_locations if session_locations else set()

    def get_next(self) -> {'MazeWalker'}:
        next_walkers = set()
        cursor = self.maze.cursor
        for action in self.ACTIONS:
            next_cursor = cursor[0] + action[0], cursor[1] + action[1]
            if next_cursor not in self.maze.walls \
                    and next_cursor not in self.session_locations \
                    and next_cursor not in self.maze.doors:

                next_walker = self.copy()
                next_walker.maze.cursor = next_cursor
                next_walker.moves += 1

                if next_cursor in self.maze.keys:
                    next_walker.session_locations = set()
                    door_name = next_walker.maze.keys[next_cursor].upper()

                    current_keys = list(self.last_found)
                    current_keys.append(door_name.lower())
                    self.last_found = tuple(current_keys)
                    self.found_keys[self.last_found] = self.moves

                    del next_walker.maze.keys[next_cursor]
                    doors = next_walker.maze.doors
                    for door_loc in doors.copy():
                        if doors[door_loc] == door_name:
                            del doors[door_loc]
                            break
                else:
                    next_walker.session_locations.add(cursor)

                next_walkers.add(next_walker)
        return next_walkers

    def matches_found(self, found: {(str, ...): (int, 'MazeWalker')}) -> bool:
        if len(self.last_found) > 0:
            for target in self.found_keys:
                if target in found:
                    value = self.found_keys[target]
                    if found[target] > value:
                        found[target] = value
                        return True
                    elif found[target] == value:
                        return True
                    else:
                        return False
                else:
                    found[target] = self.found_keys[target]
                    return True
        else:
            return True

    def is_finished(self):
        return len(self.maze.keys) == 0

    def copy(self):
        return MazeWalker(self.maze.copy(), self.moves, self.found_keys.copy(),
                          self.last_found, self.session_locations.copy())


def solve_maze(maze: Maze):
    found: {(str, ...): (int, MazeWalker)} = {}
    working: {MazeWalker} = {MazeWalker(maze)}

    while len(working) > 0:
        temp_working = working.copy()
        working = set()
        for target in temp_working:
            if not target.is_finished():
                for next_target in target.get_next():
                    if next_target.matches_found(found):
                        working.add(next_target)
            else:
                return target.moves


def part1():
    maze: Maze = read_maze_from_file()
    print(maze.get_splits())
    print(maze.get_dead_ends())


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
