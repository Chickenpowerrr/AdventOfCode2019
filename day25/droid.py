from day25.input import INSTRUCTIONS
from intcode.computer import Computer


class DroidScriptHandler:

    def __init__(self):
        self.action = ''
        self.line = ''

    def handle_input(self) -> int:
        if self.action:
            character = self.action[0]
            self.action = self.action[1:]
            return ord(character)
        else:
            self.action = input('> ') + '\n'
            return self.handle_input()

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
    instructions = INSTRUCTIONS.copy()
    droidScript: DroidScriptHandler = DroidScriptHandler()
    computer: Computer = Computer(instructions, droidScript.handle_input, droidScript.handle_output)
    computer.execute()


def part2():
    pass


if __name__ == '__main__':
    part1()
    part2()
