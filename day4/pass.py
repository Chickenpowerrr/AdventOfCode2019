def is_valid(pass_phrase: str) -> bool:
    last = pass_phrase[0]
    adjunct = False

    for char in pass_phrase[1:]:
        if int(last) > int(char):
            return False
        elif int(last) == int(char):
            adjunct = True
        last = char
    return adjunct


def is_valid_2(pass_phrase: str) -> bool:
    last = pass_phrase[0]
    adjunct = False

    for i in range(1, len(pass_phrase)):
        if int(last) == int(pass_phrase[i]):
            if (i - 2 < 0 or int(pass_phrase[i - 2]) != int(last)) and (
                    i + 1 >= len(pass_phrase) or int(last) != int(pass_phrase[i + 1])):
                adjunct = True
        elif int(last) > int(pass_phrase[i]):
            return False
        last = pass_phrase[i]
    return adjunct


count = 0
for j in range(356261, 846303):
    if is_valid_2(str(j)):
        count += 1
print(count)
