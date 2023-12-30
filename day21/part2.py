from math import ceil

import networkx as nx

from utils import read_input

type Pos = tuple[int, int]


# real input is 131 x 131 lines with S at exact center (65, 65)
# required number of steps is 26501365
# which is 202300 * 131 + 65
# (okay I read that on reddit)

# quadratic solution (like the area of a circle), so we need 3 points for a solution
# 65, 196, 327
# for the last one I'll need 5x5 times the original grid

def multiply_grid(lines: list[str], factor: int) -> list[str]:
    assert factor % 2 == 1
    big_grid = []
    for _ in range(factor):
        for line in lines:
            big_grid.append(line * factor)

    return big_grid


def count_plots(lines: list[str], steps: int) -> int:
    orig_grid_size = len(lines)
    min_target_grid_size = steps * 2 + 1
    grid_factor = ceil(min_target_grid_size / orig_grid_size)
    if grid_factor % 2 == 0:
        grid_factor += 1

    lines = multiply_grid(lines, grid_factor)

    plot_points = [(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char in "S."]

    start_points = [(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "S"]
    start = start_points[grid_factor ** 2 // 2]  # middle one
    print(f"Starting node is {start}")

    graph = nx.Graph()
    graph.add_nodes_from(plot_points)
    for x, y in graph:
        for dx, dy in [(1, 0), (0, 1)]:
            if (x + dx, y + dy) in graph:
                graph.add_edge((x, y), (x + dx, y + dy))

    ego_graph = nx.ego_graph(graph, n=start, radius=steps)
    # checkerboard rule, plot counts if both x and y are odd, or both are even; can be checked if x+y is even
    # THIS ONLY WORKS FOR EVEN STEP COUNTS! FOR ODD STEP COUNTS IT'S EXACTLY THE OTHER WAY AROUND
    if steps % 2 == 0:
        return sum(1 for x, y in ego_graph if (x + y) % 2 == 0)
    else:
        return sum(1 for x, y in ego_graph if (x + y) % 2 == 1)


def part2(lines: list[str]) -> int:
    p = {k: count_plots(lines, 65 + 131 * k) for k in range(3)}
    print(p)

    # did some maths on paper to solve for P = a*k**2 + b*k + c
    a = (p[2] - 2 * p[1] + p[0]) / 2
    b = (-2 * p[2] + 4 * p[1] - 3 * p[0]) / 2
    c = p[0]

    target_k = (26501365 - 65) / 131  # 202300
    return int(a * target_k ** 2 + b * target_k + c)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert count_plots(test_lines, 6) == 16
    assert count_plots(test_lines, 10) == 50
    assert count_plots(test_lines, 50) == 1594
    assert count_plots(test_lines, 100) == 6536
    assert count_plots(test_lines, 500) == 167004

    input_lines = read_input("input.txt")
    print(part2(input_lines))
