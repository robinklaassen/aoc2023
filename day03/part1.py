from utils import read_input


def get_part_numbers(schematic: list[str]) -> list[int]:
    part_numbers = []

    number_positions = get_number_positions(schematic)
    for line_idx, min_idx, max_idx in number_positions:
        if number_has_adjacent_symbol(schematic, line_idx, min_idx, max_idx):
            line = schematic[line_idx]
            number = line[min_idx:max_idx + 1]
            part_numbers.append(int(number))

    return part_numbers


def get_number_positions(schematic: list[str]) -> list[tuple[int, int, int]]:
    # position tuples are (line index, min char index, max char index)
    positions = []
    for line_idx, line in enumerate(schematic):
        for char_idx, char in enumerate(line):
            if not char.isnumeric():
                continue

            number_idxs = find_number_idxs(line, char_idx)
            # number = int(line[number_idxs[0]:number_idxs[1]+1])
            position = line_idx, *number_idxs
            if position not in positions:
                positions.append(position)

    return positions


def number_has_adjacent_symbol(schematic: list[str], line_idx: int, min_idx: int, max_idx: int) -> bool:
    for char_idx in range(min_idx, max_idx + 1):
        if char_has_adjacent_symbol(schematic, line_idx, char_idx):
            return True
    return False


def char_has_adjacent_symbol(schematic: list[str], line_idx: int, char_idx: int) -> bool:
    adj_positions = generate_adj_positions((line_idx, char_idx))
    for pos in adj_positions:
        try:
            char = schematic[pos[0]][pos[1]]
        except IndexError:
            continue

        if is_symbol(char):
            return True
    return False


def is_symbol(char: str) -> bool:
    return not char.isnumeric() and char != "."


def find_number_idxs(line: str, char_idx: int) -> tuple[int, int]:
    min_idx = char_idx
    while min_idx != 0 and line[min_idx - 1].isnumeric():
        min_idx -= 1

    max_idx = char_idx
    while max_idx != len(line) - 1 and line[max_idx + 1].isnumeric():
        max_idx += 1

    return min_idx, max_idx


def generate_adj_positions(position: tuple[int, int]):
    line, char = position
    for line_idx in [line - 1, line, line + 1]:
        for char_idx in [char - 1, char, char + 1]:
            if line_idx != -1 and char_idx != -1:
                yield line_idx, char_idx


if __name__ == "__main__":
    test_input = read_input("input_test1.txt")
    test_part_numbers = get_part_numbers(test_input)
    assert sum(test_part_numbers) == 4361

    input_lines = read_input("input.txt")
    part_numbers = get_part_numbers(input_lines)

    print(f"Sum of part numbers: {sum(part_numbers)}")
