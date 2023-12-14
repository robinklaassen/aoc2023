from itertools import pairwise

from utils import read_input, transpose_grid, find_indexes


def part1(lines: list[str]) -> int:
    grid = transpose_grid(lines)

    total_load = 0

    for col in grid:
        rounds = find_indexes(col, "O")
        blocks = find_indexes(col, "#")

        for b1, b2 in pairwise([-1] + blocks + [len(col)]):
            num_rounds = sum(1 for r in rounds if b1 < r < b2)
            for offset in range(num_rounds):
                total_load += len(col) - offset - (b1 + 1)

    return total_load


if __name__ == "__main__":
    test_input = read_input("test_input.txt")
    assert part1(test_input) == 136

    input_lines = read_input("input.txt")
    print(part1(input_lines))
