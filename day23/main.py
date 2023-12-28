from utils import read_input

import networkx as nx

type Pos = tuple[int, int]


def construct_graph(lines: list[str], ignore_slopes: bool = False) -> tuple[nx.DiGraph, Pos, Pos]:
    # this could be a dict comprehension but I'm tired
    charmap = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != "#":
                charmap[(x, y)] = char

    graph = nx.DiGraph()
    for x, y in charmap:
        char = charmap[(x, y)]
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if not ignore_slopes and (char, dx, dy) in [
                # don't add opposite directions
                (">", -1, 0),
                ("<", 1, 0),
                ("^", 0, 1),
                ("v", 0, -1),
            ]:
                continue
            graph.add_edge((x, y), (x + dx, y + dy))

    start_node = next((x, y) for x, y in charmap if y == 0)
    end_node = next((x, y) for x, y in charmap if y == len(lines) - 1)

    return graph, start_node, end_node


def part1(lines: list[str]) -> int:
    graph, start_node, end_node = construct_graph(lines)

    assert nx.has_path(graph, start_node, end_node)
    path_lengths = [len(p) - 1 for p in nx.all_simple_paths(graph, start_node, end_node)]  # -1 is to exclude start
    return max(path_lengths)


def part2(lines: list[str]) -> int:
    # this could be a dict comprehension but I'm tired
    charmap = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != "#":
                charmap[(x, y)] = char

    graph = nx.Graph()
    for x, y in charmap:
        # char = charmap[(x, y)]
        for dx, dy in [(1, 0), (0, 1)]:
            graph.add_edge((x, y), (x + dx, y + dy))

    start_node = next((x, y) for x, y in charmap if y == 0)
    end_node = next((x, y) for x, y in charmap if y == len(lines) - 1)

    assert nx.has_path(graph, start_node, end_node)
    max_length = 0
    for p in nx.all_simple_paths(graph, start_node, end_node):
        length = len(p) - 1
        if length > max_length:
            max_length = length
            print(length)

    return max_length


if __name__ == "__main__":
    test_lines = read_input("test.txt")
    assert part1(test_lines) == 94

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    # wow this is slow
    assert part2(test_lines) == 154
    print(part2(input_lines))
