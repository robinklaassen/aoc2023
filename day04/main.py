from functools import cache
from queue import SimpleQueue

from utils import read_input


def get_points_total(lines: list[str]) -> int:
    points = [get_card_points(line) for line in lines]
    return sum(points)


def get_card_points(line: str) -> int:
    matches = get_card_matches(line)
    return 2 ** (len(matches) - 1) if matches else 0


@cache  # very much needed for part 2
def get_card_matches(line: str) -> list[int]:
    card_str, all_numbers = line.split(": ")
    card_id = card_str.split(" ")[1]
    win_str, have_str = all_numbers.split(" | ")

    win_nums = [int(num) for num in win_str.split(" ") if num]
    have_nums = [int(num) for num in have_str.split(" ") if num]

    return [num for num in have_nums if num in win_nums]


def get_total_cards_new_rules(lines: list[str]) -> int:
    card_queue = SimpleQueue()
    for idx, line in enumerate(lines):
        card_queue.put((idx, line))

    card_count = 0
    while not card_queue.empty():
        idx, line = card_queue.get()
        card_count += 1
        matches = get_card_matches(line)
        if not matches:
            continue

        for new_idx in range(idx + 1, idx + 1 + len(matches)):
            card_queue.put((new_idx, lines[new_idx]))

    return card_count


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    test_points = get_points_total(test_lines)
    assert test_points == 13

    input_lines = read_input("input.txt")
    print(get_points_total(input_lines))

    # part 2
    assert get_total_cards_new_rules(test_lines) == 30
    print(get_total_cards_new_rules(input_lines))
