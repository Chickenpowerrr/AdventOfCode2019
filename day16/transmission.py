from day16.input import NUMBER


def get_setting(length: int, phase: int) -> [int]:
    result = []
    start = phase - 1
    for i in range(length + 1):
        target = i % (4 * phase)
        if target <= start:
            result.append(0)
        elif start < target <= start + phase:
            result.append(1)
        elif start + phase < target <= start + 2 * phase:
            result.append(0)
        else:
            result.append(-1)
    return result[1:]


def apply_signal(signal: str) -> str:
    result = ''
    ints = [int(i) for i in signal]
    length = len(signal)
    for phase in range(1, length + 1):
        setting = get_setting(length, phase)
        result += str(sum([ints[i] * setting[i] for i in range(length)]))[-1]
    return result


def apply_signal_tail(signal):
    if type(signal) == str:
        signal = [int(char) for char in signal]
    length = len(signal)
    for i in range(length - 2, -1, -1):
        signal[i] = int(str((signal[i] + signal[i + 1]))[-1])
    return signal


def calculate_offset(signal: str) -> int:
    return int(''.join([char for char in signal[:7]]))


def part1():
    value = NUMBER
    for _ in range(100):
        value = apply_signal(value)
    print(f'First 8 digits: {value[:8]}')


def part2():
    value = NUMBER
    value = (value * 10_000)[calculate_offset(value):]
    for _ in range(100):
        value = apply_signal_tail(value)
    print(f'Decoded: {"".join([str(i) for i in value])[:8]}')


if __name__ == '__main__':
    part1()
    part2()
