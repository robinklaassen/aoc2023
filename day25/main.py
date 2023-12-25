from utils import read_input

import networkx as nx

from ipysigma import Sigma


def part1(lines: list[str]):
    graph = nx.Graph()

    for line in lines:
        left, right = line.split(": ")
        for target in right.split(" "):
            graph.add_edge(left, target)

    sigma = Sigma(graph, height=1000, start_layout=10)
    sigma.to_html("graph.html")

    # visually determined thanks to magic layouting of Sigma
    edges_to_remove = [
        ("mfc", "vph"),
        ("fql", "rmg"),
        ("sfm", "vmt"),
    ]

    graph.remove_edges_from(edges_to_remove)
    islands = list(nx.connected_components(graph))
    assert len(islands) == 2
    print(len(islands[0]) * len(islands[1]))


if __name__ == "__main__":
    input_lines = read_input("input.txt")
    part1(input_lines)
