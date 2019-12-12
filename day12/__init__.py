def get_possibilities(values: [int], suppliers: int, total: int):
    result = []
    cursors = [values[0] for _ in range(suppliers)]
    while cursors[0] < len(values):
        current = -1
        while True:
            if abs(current) <= len(cursors):
                if cursors[current] < len(values) - 1:
                    cursors[current] += 1
                    attempt = [values[cursor] for cursor in cursors]
                    if sum(attempt) == total:
                        if set(attempt) not in result:
                            result.append(set(attempt))
                    break
                else:
                    cursors[current] = values[0]
                    current -= 1
            else:
                return result
    return result


print(len(get_possibilities(range(-1, 6), 4, 8)))
print(len(get_possibilities(range(-10, 6), 4, -13)))
print(len(get_possibilities(range(-7, 9), 4, 2)))
