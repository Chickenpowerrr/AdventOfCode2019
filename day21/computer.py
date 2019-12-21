import sys

from day21.input import INSTRUCTIONS
from intcode.computer import Computer


class JumpScriptHandler:

    def __init__(self, walk: bool = True):
        # Check if 1 not available or (2 or 3 not available and 4 available)
        self.walk_actions = [
            # Check if 3 not available
            'NOT C T',
            # Check if 2 not available
            'NOT B J',
            # Check if 2 or 3 not available
            'OR T J',
            # Check if 4 is available
            'AND D J',
            # Check if 1 is not available
            'NOT A T',
            # Check if 1 not available or (2 or 3 not available and 4 available)
            'OR T J',
            # Start walking
            'WALK'
        ]

        # Check if 1 not available or (2 or 3 not available and 4 and 8 available)
        self.run_actions = [
            # Check if 3 not available
            'NOT C T',
            # Check if 2 not available
            'NOT B J',
            # Check if 2 or 3 not available
            'OR T J',
            # Check if 4 is available
            'AND D J',
            # Check if 8 is available
            'AND H J',
            # Check if 1 is not available
            'NOT A T',
            # Check if 1 not available or (2 or 3 not available and 4 available)
            'OR T J',
            # Start walking
            'RUN'
        ]

        self.walk = walk
        self.action_cursor = 0
        self.char_cursor = 0
        self.line = ''

    def handle_input(self) -> int:
        actions = self.walk_actions if self.walk else self.run_actions

        if self.action_cursor < len(actions):
            action = actions[self.action_cursor]
            if self.char_cursor < len(action):
                character = action[self.char_cursor]
                self.char_cursor += 1
                return ord(character)
            else:
                self.char_cursor = 0
                self.action_cursor += 1
                return ord('\n')
        else:
            print('ERROR: No new input')
            sys.exit()

    def handle_output(self, output: int):
        try:
            character = str(chr(output))
            if character != '\n':
                self.line += character
            else:
                print(self.line)
                self.line = ''
        except ValueError:
            print(f'Amount of hull damage: {output}')


def part1():
    script_handler: JumpScriptHandler = JumpScriptHandler(True)
    instructions = INSTRUCTIONS.copy()
    computer: Computer = Computer(instructions,
                                  script_handler.handle_input,
                                  script_handler.handle_output)
    computer.execute()


def part2():
    script_handler: JumpScriptHandler = JumpScriptHandler(False)
    instructions = INSTRUCTIONS.copy()
    computer: Computer = Computer(instructions,
                                  script_handler.handle_input,
                                  script_handler.handle_output)
    computer.execute()


if __name__ == '__main__':
    part1()
    part2()
