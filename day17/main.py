from heapq import heappop, heappush

from utils import read_input

type Point = tuple[int, int]
type HeapItem = tuple[int, int, int, int, int]  # total_heat, x, y, parent_x, parent_y


def modded_dijkstra(values: dict[Point, int], start: Point, end: Point) -> int:
    start_x, start_y = start
    queue: list[HeapItem] = [(0, start_x, start_y, 0, 0)]
    visited: set[tuple[int, int, int, int]] = set()

    while queue:
        heat, x, y, px, py = heappop(queue)  # get item with the lowest total heat

        # (px, py) is to keep track of the direction you came from, they are not nodes but cardinal directions
        # print(f"Heat:{heat}, pos:{(x, y)}, parent_delta:{(px, py)}")

        if (x, y) == end:
            return heat

        if (x, y, px, py) in visited:
            continue

        visited.add((x, y, px, py))

        # loop through cardinal directions, but skip forward and back
        # (so keep 2 directions perpendicular, or all from starting position where px, py = 0, 0)
        for dx, dy in {(1, 0), (0, 1), (-1, 0), (0, -1)} - {(px, py), (-px, -py)}:
            a, b, h = x, y, heat
            for i in range(1, 4):
                a, b = a + dx, b + dy
                if not (a, b) in values:
                    # no going out of town
                    continue
                h += values[(a, b)]
                heappush(queue, (h, a, b, dx, dy))

    raise IndexError("Queue exhausted")


def part1(lines: list[str]) -> int:
    heat_values = {(x, y): int(c) for y, line in enumerate(lines) for x, c in enumerate(line)}

    xsize = len(lines[0])
    ysize = len(lines)

    return modded_dijkstra(heat_values, (0, 0), (xsize - 1, ysize - 1))


if __name__ == "__main__":
    simple_lines = read_input("simple_input.txt")
    assert part1(simple_lines) == 26

    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 102

    input_lines = read_input("input.txt")
    print(part1(input_lines))
