import functools
from collections import Counter

from utils import read_input

SINGLE_CARD_STRENGTH = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


@functools.total_ordering
class Hand:
    def __init__(self, line: str):
        cards, bid = line.split(" ")
        self.cards: list[str] = list(cards)
        self.bid: int = int(bid)

    @property
    def cards_type(self) -> int:
        count = Counter(self.cards)
        counts = list(count.values())
        match sorted(counts, reverse=True):
            case [5]:
                return 7
            case [4, 1]:
                return 6
            case [3, 2]:
                return 5
            case [3, 1, 1]:
                return 4
            case [2, 2, 1]:
                return 3
            case [2, 1, 1, 1]:
                return 2
            case [1, 1, 1, 1, 1]:
                return 1
            case _:
                raise Exception("wtf")

    def __lt__(self, other):
        if self.cards_type < other.cards_type:
            return True
        if self.cards_type == other.cards_type:
            for i in range(5):
                self_card = self.cards[i]
                other_card = other.cards[i]
                if SINGLE_CARD_STRENGTH.index(self_card) < SINGLE_CARD_STRENGTH.index(other_card):
                    return True
                if SINGLE_CARD_STRENGTH.index(self_card) > SINGLE_CARD_STRENGTH.index(other_card):
                    return False
        return False

    def __eq__(self, other):
        return sorted(self.cards) == sorted(other.cards)


def total_winnings(lines: list[str]) -> int:
    hands = [Hand(line) for line in lines]
    hands = sorted(hands)
    print([hand.cards for hand in hands])

    winnings = 0
    for idx, hand in enumerate(hands):
        winnings += (idx + 1) * hand.bid
    return winnings


if __name__ == "__main__":
    assert Hand("QQQJA 123") > Hand("T55J5 123")
    assert Hand("2K975 1") > Hand("2954J 1")

    test_lines = read_input("test_input.txt")
    assert total_winnings(test_lines) == 6440

    input_lines = read_input("input.txt")
    print(total_winnings(input_lines))
