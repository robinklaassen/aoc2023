from itertools import pairwise

from utils import read_input

type Point = tuple[int, int]

DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def dig_trench(lines: list[str]) -> tuple[list[Point], int]:
    x, y = 0, 0
    vertices: list[Point] = [(x, y)]
    perimeter: int = 0
    # dig out trench
    for line in lines:
        step_dir, step_count, color = line.split(" ")
        step_count = int(step_count)

        dx, dy = DIRECTIONS[step_dir]
        x, y = x + (step_count * dx), y + (step_count * dy)
        vertices.append((x, y))

        perimeter += step_count

    return vertices, perimeter


def dig_bigger_trench(lines: list[str]) -> tuple[list[Point], int]:
    x, y = 0, 0
    vertices: list[Point] = [(x, y)]
    perimeter: int = 0
    # dig out trench
    for line in lines:
        hex_code = line.split("#")[1].rstrip(")")
        step_count = int(hex_code[:-1], 16)
        step_dir = ["R", "D", "L", "U"][int(hex_code[-1])]

        dx, dy = DIRECTIONS[step_dir]
        x, y = x + (step_count * dx), y + (step_count * dy)
        vertices.append((x, y))

        perimeter += step_count

    return vertices, perimeter


def shoelace(vertices: list[Point]) -> int:
    assert vertices[-1] == vertices[0]

    volume = 0

    for v1, v2 in pairwise(vertices):
        x1, y1 = v1
        x2, y2 = v2
        volume += (x1 * y2) - (x2 * y1)

    return int(volume / 2)


def part1(lines: list[str]) -> int:
    grid, perimeter = dig_trench(lines)

    shoelace_volume = shoelace(grid)

    result = shoelace_volume + int(perimeter / 2) + 1

    return result


def part2(lines: list[str]) -> int:
    grid, perimeter = dig_bigger_trench(lines)

    shoelace_volume = shoelace(grid)

    result = shoelace_volume + int(perimeter / 2) + 1

    return result


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 62

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    assert part2(test_lines) == 952408144115
    print(part2(input_lines))
