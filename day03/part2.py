from day03.part1 import get_number_positions
from utils import read_input


def get_gears(schematic: list[str]) -> list[tuple[int, int]]:
    gears = []
    gear_positions = get_gear_positions(schematic)
    number_positions = get_number_positions(schematic)

    for gear_pos in gear_positions:
        adj_numbers = [number_pos for number_pos in number_positions if gear_and_number_adjacent(gear_pos, number_pos)]
        if len(adj_numbers) != 2:
            continue

        numbers = [get_number_from_pos(schematic, number_pos) for number_pos in adj_numbers]
        gears.append(tuple(numbers))

    return gears


def get_gear_positions(schematic: list[str]) -> list[tuple[int, int]]:
    # position tuples are (line index, character index)
    positions = []
    for line_idx, line in enumerate(schematic):
        for char_idx, char in enumerate(line):
            if char == "*":
                positions.append((line_idx, char_idx))
    return positions


def gear_and_number_adjacent(gear_pos: tuple[int, int], number_pos: tuple[int, int, int]) -> bool:
    gear_line_idx, gear_char_idx = gear_pos
    num_line_idx, num_min_idx, num_max_idx = number_pos

    if abs(gear_line_idx - num_line_idx) > 1:
        return False

    if num_max_idx < gear_char_idx - 1:
        return False

    if num_min_idx > gear_char_idx + 1:
        return False

    return True


def get_number_from_pos(schematic: list[str], number_pos: tuple[int, int, int]) -> int:
    line_idx, min_idx, max_idx = number_pos
    line = schematic[line_idx]
    return int(line[min_idx:max_idx + 1])


def add_gear_ratios(gears: list[tuple[int, int]]) -> int:
    result = 0
    for gear in gears:
        result += gear[0] * gear[1]
    return result


if __name__ == "__main__":
    test_input = read_input("input_test1.txt")
    test_gears = get_gears(test_input)
    print(test_gears)

    assert add_gear_ratios(test_gears) == 467835

    input_lines = read_input("input.txt")
    gears = get_gears(input_lines)
    print(gears)
    print(add_gear_ratios(gears))
