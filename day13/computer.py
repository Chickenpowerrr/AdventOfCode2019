from day13.input import INSTRUCTIONS
from intcode.computer import Computer


class Game:

    def __init__(self):
        self.score = 0
        self.output_target = []
        self.items = {}

    def handle_input(self) -> int:
        delta = [item for item in self.items if self.items[item] == 4][0][0] - \
                [item for item in self.items if self.items[item] == 3][0][0]

        return 1 if delta > 0 else -1 if delta < 0 else 0

    def handle_output(self, value: int):
        if len(self.output_target) < 2:
            self.output_target.append(value)
        else:
            if self.output_target[0] == -1 and self.output_target[1] == 0:
                self.output_target = []
                if value > 0:
                    self.score = value
            else:
                self.items[(self.output_target[0], self.output_target[1])] = value
                self.output_target = []

    def count_type(self, item: int) -> int:
        return len({tar for tar in self.items if self.items[tar] == item})


def part1():
    instructions: [int] = INSTRUCTIONS.copy()
    game: Game = Game()
    computer: Computer = Computer(instructions, game.handle_input, game.handle_output)
    computer.execute()
    print(f'Block tiles: {game.count_type(2)}')


def part2():
    instructions: [int] = INSTRUCTIONS.copy()
    instructions[0] = 2
    game: Game = Game()
    computer: Computer = Computer(instructions, game.handle_input, game.handle_output)
    computer.execute()
    print(f'Final score: {game.score}')


if __name__ == '__main__':
    part1()
    part2()
