import sys


class Deck:

    def __init__(self, cards=10_007):
        self.cards = [i for i in range(cards)]

    def new_stack(self):
        self.cards = list(reversed(self.cards))

    def cut(self, n: int):
        new_cards = self.cards[n:]
        new_cards.extend(self.cards[:n])
        self.cards = new_cards

    def increment(self, n: int):
        new_cards = self.cards.copy()
        i = 0
        for card in self.cards:
            new_cards[i] = card
            i = (i + n) % len(new_cards)
        self.cards = new_cards

    def __str__(self):
        return str(self.cards)


class SimulatedIncrementer:

    def __init__(self, n: int, modulo: int):
        self.n = n
        self.modulo = modulo
        self.base = self.modulo + self.n
        self.base_rows = self.calculate_base_rows()
        self.order = self.calculate_order()

    def calculate_base_rows(self):
        new_cards = [1]
        i = 0

        for _ in range(self.base - 1):
            previous = i
            i = (i + self.n) % self.base
            if previous < i:
                new_cards[-1] += 1
            else:
                new_cards.append(1)

        if len(new_cards) == self.n:
            return new_cards
        else:
            self.base += self.n
            return self.calculate_base_rows()

    def calculate_order(self):
        cards = list(range(self.base))
        new_cards = cards.copy()

        i = 0
        for card in cards:
            new_cards[i] = card
            i = (i + self.n) % len(new_cards)

        order = new_cards[:self.n]
        sorted_head = list(sorted(order))
        return list(map(sorted_head.index, order))

    def reverse(self, target: int, cards: int):
        found_row = self.order[target % self.n]
        relative = target // self.n

        difference = (cards - self.base) // self.n
        return sum([row + difference for row in self.base_rows][:found_row]) + relative

    def apply(self, target: int, cards: int) -> int:
        difference = (cards - self.base) // self.n
        rows = [row + difference for row in self.base_rows]

        previous_count = 0
        found_row = 0
        relative = 0

        for row in rows:
            if target >= previous_count + row:
                previous_count += row
                found_row += 1
            else:
                relative = target - previous_count
                break

        return self.order.index(found_row) + relative * self.n


class SimulatedDeck:
    INCREMENTERS: {(int, int): SimulatedIncrementer} = {}

    def __init__(self, target=2020, cards=119315717514047):
        self.cards = cards
        self.target = target

    def new_stack(self):
        self.target = self.cards - self.target - 1

    def cut(self, n: int):
        if n > 0:
            if n > self.target:
                self.target += self.cards - n
            else:
                self.target -= n
        else:
            self.cut(self.cards + n)

    def increment(self, n: int):
        modulo = self.cards % n
        if (n, modulo) not in self.INCREMENTERS:
            self.INCREMENTERS[(n, modulo)] = SimulatedIncrementer(n, modulo)

        incrementer = self.INCREMENTERS[(n, modulo)]
        self.target = incrementer.apply(self.target, self.cards)


class BackPropagatingDeck:
    INCREMENTERS: {(int, int): SimulatedIncrementer} = {}

    def __init__(self, cursor: int, cards: int):
        self.cursor = cursor
        self.cards = cards

    def new_stack(self):
        self.cursor = self.cards - self.cursor - 1

    def cut(self, n: int):
        if n > 0:
            if n > self.cards - self.cursor - 1:
                self.cursor -= self.cards - n
            else:
                self.cursor += n
        else:
            self.cut(self.cards + n)

    def increment(self, n: int):
        modulo = self.cards % n
        if (n, modulo) not in self.INCREMENTERS:
            self.INCREMENTERS[(n, modulo)] = SimulatedIncrementer(n, modulo)

        incrementer = self.INCREMENTERS[(n, modulo)]
        self.cursor = incrementer.reverse(self.cursor, self.cards)


def execute_instructions(deck, instructions: [(int, int)]):
    for instruction in instructions:
        if instruction[0] == 1:
            deck.cut(instruction[1])
        elif instruction[0] == 2:
            deck.increment(instruction[1])
        elif instruction[0] == 3:
            deck.new_stack()
        else:
            print(f'ERROR: invalid instruction: {instruction}')
            sys.exit()


def get_instructions() -> [(int, int)]:
    result = []
    with open('input.txt') as file:
        for line in file.readlines():
            line = line.strip()
            if line.startswith('cut'):
                n = int(line.split(' ')[1])
                result.append((1, n))
            elif line.startswith('deal with increment'):
                n = int(line.split(' ')[3])
                result.append((2, n))
            elif line.startswith('deal into new stack'):
                result.append((3, 0))
            else:
                print(f'ERROR: invalid input {line}')
                sys.exit()
    return result


def part1():
    deck = SimulatedDeck(2019, 10_007)
    execute_instructions(deck, get_instructions())
    print(f'Index of 2019: {deck.target}')


def part2():
    instructions = get_instructions()[::-1]

    deck: BackPropagatingDeck = BackPropagatingDeck(2020, 119315717514047)
    history = set()

    i = 0
    while deck.cursor not in history:
        history.add(deck.cursor)

        i += 1
        if i % 10_000 == 0:
            print(f'Processed {i}...')

        execute_instructions(deck, instructions)

    print(f'Found: {i} -> {deck.cursor}')


if __name__ == '__main__':
    part1()
    part2()
