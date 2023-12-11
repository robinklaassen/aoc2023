from itertools import combinations

from utils import read_input


def solve(lines: list[str], expand_factor: int = 2) -> int:
    # don't expand the entire universe, just amend the galaxy positions smart boi
    original_galaxy_positions = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                original_galaxy_positions.append((x, y))

    empty_row_idxs = []
    for y, line in enumerate(lines):
        if len(set(line)) == 1:
            empty_row_idxs.append(y)

    empty_col_idxs = []
    for x in range(len(lines[0])):
        col = [line[x] for line in lines]
        if len(set(col)) == 1:
            empty_col_idxs.append(x)

    expanded_galaxy_positions = []
    for pos in original_galaxy_positions:
        new_x, new_y = pos
        for x in empty_col_idxs:
            if x < pos[0]:
                new_x += expand_factor - 1
        for y in empty_row_idxs:
            if y < pos[1]:
                new_y += expand_factor - 1
        expanded_galaxy_positions.append((new_x, new_y))

    # the rest is trivial with itertools <3
    shortest_path_sum = 0
    for p1, p2 in combinations(expanded_galaxy_positions, 2):
        shortest_path_sum += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    return shortest_path_sum


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert solve(test_lines) == 374

    input_lines = read_input("input.txt")
    print(solve(input_lines))

    # part 2

    assert solve(test_lines, 10) == 1030
    assert solve(test_lines, 100) == 8410
    print(solve(input_lines, int(1e6)))
