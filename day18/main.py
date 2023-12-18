from utils import read_input

type Point = tuple[int, int]

DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def dig_trench(lines: list[str]) -> list[Point]:
    x, y = 0, 0
    grid: list[Point] = [(x, y)]
    # dig out trench
    for line in lines:
        step_dir, step_count, color = line.split(" ")
        dx, dy = DIRECTIONS[step_dir]
        for _ in range(int(step_count)):
            x += dx
            y += dy
            grid.append((x, y))
    return grid


def dig_bigger_trench(lines: list[str]) -> list[Point]:
    x, y = 0, 0
    grid: list[Point] = [(x, y)]
    # dig out trench
    for line in lines:
        hex_code = line.split("#")[1].rstrip(")")
        step_count = int(hex_code[:-1], 16)
        step_dir = ["R", "D", "L", "U"][int(hex_code[-1])]

        dx, dy = DIRECTIONS[step_dir]
        for _ in range(int(step_count)):
            x += dx
            y += dy
            grid.append((x, y))
    return grid


def determine_volume(grid: list[Point]) -> int:
    # determine corners
    min_x = min(x for x, y in grid)
    min_y = min(y for x, y in grid)
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)

    volume = 0

    for y in range(min_y, max_y + 1):
        inside = False
        prev_corner_dir = None
        line = ""
        for x in range(min_x, max_x + 1):
            is_trench = (x, y) in grid

            # count the spaaaace
            if is_trench or inside:
                volume += 1

            # fancy printing stuff
            if is_trench:
                line += "#"
            else:
                line += ("O" if inside else ".")

            if not is_trench:
                continue

            # determine type of trench we're in
            above_is_trench = (x, y - 1) in grid
            below_is_trench = (x, y + 1) in grid

            if above_is_trench and below_is_trench:
                trench_type = "|"
            elif above_is_trench:
                trench_type = "U"
            elif below_is_trench:
                trench_type = "D"
            else:
                trench_type = "-"

            if trench_type == "|":
                # cross border on vertical path
                inside = not inside
                continue
            elif trench_type == "-":
                continue

            # trench type is now certainly a corner
            if prev_corner_dir is None:
                prev_corner_dir = trench_type
                continue

            # there was a previous corner in this trench
            if prev_corner_dir != trench_type:
                inside = not inside

            prev_corner_dir = None

        # print(line)
    return volume


def part1(lines: list[str]) -> int:
    grid = dig_trench(lines)

    volume = determine_volume(grid)

    return volume


def part2(lines: list[str]) -> int:
    grid = dig_bigger_trench(lines)

    volume = determine_volume(grid)

    return volume


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 62

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    assert part2(test_lines) == 952408144115  # nope does not perform, as expected
