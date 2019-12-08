from day8.input import ENCODED


def split(encoded: int, width: int, length: int) -> [[str]]:
    encoded: str = str(encoded)
    layers: [[str]] = []
    temp: [str] = []
    for i in range(0, int(len(encoded) / width)):
        temp.append(encoded[i * width:(i + 1) * width])
        if len(temp) >= length:
            layers.append(temp)
            temp: [str] = []
    return layers


def fewest(split_file: [[str]]) -> [str]:
    min_count = None
    min_layer = None
    for layer in split_file:
        count = sum([row.count('0') for row in layer])
        if min_count is None or count < min_count:
            min_count = count
            min_layer = layer
    print(min_layer)
    return min_layer


def get_hash(split_file: [[str]]) -> int:
    target_layer: [str] = fewest(split_file)
    return sum([row.count('1') for row in target_layer]) \
           * sum([row.count('2') for row in target_layer])


def decode(split_file: [[str]], width, height) -> [str]:
    result: [[str]] = [[] for _ in range(0, height)]
    for row in range(0, height):
        for column in range(0, width):
            for entry in split_file:
                if entry[row][column] != '2':
                    result[row].append(entry[row][column])
                    break
    return result


def render(decoded: [str]):
    for row in decoded:
        visual_row = ''
        for pixel in row:
            visual_row += pixel.replace('0', '-').replace('1', '*')
        print(visual_row)


value: int = ENCODED
print(split(value, 25, 6))
print(decode(split(value, 25, 6), 25, 6))
render(decode(split(value, 25, 6), 25, 6))
