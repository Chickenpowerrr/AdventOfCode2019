import itertools

from day7.input import INSTRUCTIONS
from intcode.computer import Computer, InputInstruction


class SignalMonitor:

    def __init__(self):
        self.highest = 0
        self.last_output = 0
        self.setting = 0
        self.is_first = True

    def set_setting(self, setting: int):
        self.setting = setting

    def set_last_output(self, last_output: int):
        self.last_output = last_output

        if last_output > self.highest:
            self.highest = last_output

    def get_value(self):
        value = self.setting if self.is_first else self.last_output
        self.is_first = False
        return value

    def reset(self):
        self.last_output = 0
        self.setting = 0
        self.is_first = True


def part1():
    monitor: SignalMonitor = SignalMonitor()

    for permutation in itertools.permutations(range(5)):
        monitor.set_last_output(0)

        for setting in permutation:
            monitor.set_setting(setting)
            computer: Computer = Computer(INSTRUCTIONS.copy(), monitor.get_value,
                                          monitor.set_last_output)
            computer.execute()
            monitor.is_first = True
    print(monitor.highest)


def part2():
    monitor: SignalMonitor = SignalMonitor()

    for permutation in itertools.permutations(range(5, 10)):
        monitor.set_last_output(0)

        computers: [Computer] = [Computer(INSTRUCTIONS.copy(), monitor.get_value,
                                          monitor.set_last_output) for _ in
                                 range(len(permutation))]
        inputs = {}
        start = True

        while len(inputs) > 0 or start:
            for computer in computers:
                request: (InputInstruction, [int])

                if start:
                    monitor.set_setting(permutation[computers.index(computer)])
                    request: (InputInstruction, [int]) = computer.execute(True)
                else:
                    request = inputs[computers.index(computer)]

                request[0].execute(request[1])
                next_request = computer.execute(True)

                if next_request:
                    inputs[computers.index(computer)] = next_request
                else:
                    del inputs[computers.index(computer)]

                if start:
                    monitor.is_first = True

            monitor.is_first = False
            start = False
        monitor.reset()
    print(f'Highest feedback loop signal: {monitor.highest}')


if __name__ == '__main__':
    part1()
    part2()
