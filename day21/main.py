import networkx as nx
import matplotlib.pyplot as plt
from utils import read_input


def part1(lines: list[str], steps: int) -> int:
    plot_points = [(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char in "S."]
    start = next((x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "S")

    print(f"Starting node is {start}")

    graph = nx.Graph()
    graph.add_nodes_from(plot_points)
    for x, y in graph:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (x + dx, y + dy) in graph:
                graph.add_edge((x, y), (x + dx, y + dy))

    # nx.draw(graph, with_labels=True)
    # plt.show()

    ego_graph = nx.ego_graph(graph, n=start, radius=steps)

    # nx.draw(ego_graph, with_labels=True)
    # plt.show()

    # misunderstood the assignment
    count = 0
    for node in ego_graph:
        if nx.shortest_path_length(graph, start, node) % 2 == 0:
            count += 1

    return count


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines, 6) == 16

    input_lines = read_input("input.txt")
    print(part1(input_lines, 64))
