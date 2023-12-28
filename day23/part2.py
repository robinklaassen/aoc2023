from utils import read_input

import networkx as nx
import matplotlib.pyplot as plt

from ipysigma import Sigma

type Pos = tuple[int, int]


def plot_graph(graph: nx.Graph | nx.DiGraph):
    g = type(graph)()
    for n, attrs in graph.nodes(data=True):
        g.add_node(str(n), **attrs)

    for u, v, attrs in graph.edges(data=True):
        g.add_edge(str(u), str(v), **attrs)

    sigma = Sigma(g, height=1000, start_layout=3, edge_label="weight")
    sigma.to_html("graph.html")


def construct_graph(lines: list[str]) -> nx.Graph:
    graph = nx.Graph()

    nodes = [(x, y) for y, line in enumerate(lines) for x, char in enumerate(line) if char != "#"]
    graph.add_nodes_from(nodes)

    for x, y in nodes:
        for dx, dy in [(1, 0), (0, 1)]:
            if (x + dx, y + dy) in nodes:
                graph.add_edge((x, y), (x + dx, y + dy))

    return graph


def simplify_graph(graph: nx.Graph, extra_focus_nodes: list[Pos]) -> nx.Graph:
    """
    Replace simple paths of nodes between forks with a single weighted edge.
    """
    forks = [n for n in graph if graph.degree(n) > 2]
    focus_nodes = set(forks).union(extra_focus_nodes)

    simple_graph = nx.Graph()
    simple_graph.add_nodes_from(focus_nodes)

    for fn in focus_nodes:
        for nn in graph.neighbors(fn):
            steps = 1
            prev_node = fn
            while nn not in focus_nodes:
                steps += 1
                next_node = next(node for node in graph.neighbors(nn) if node != prev_node)
                prev_node = nn
                nn = next_node
            simple_graph.add_edge(fn, nn, weight=steps)

    return simple_graph


def part2(lines: list[str]) -> int:
    graph = construct_graph(lines)

    start_node = next((x, y) for x, y in graph if y == 0)
    end_node = next((x, y) for x, y in graph if y == len(lines) - 1)

    # plot_graph(graph)

    simple_graph = simplify_graph(graph, [start_node, end_node])

    plot_graph(simple_graph)

    max_length = 0
    for path in nx.all_simple_edge_paths(simple_graph, start_node, end_node):
        length = sum(simple_graph[u][v]["weight"] for u, v in path)
        if length > max_length:
            print(length)
            max_length = length

    return max_length


if __name__ == "__main__":
    test_lines = read_input("test.txt")
    assert part2(test_lines) == 154

    input_lines = read_input("input.txt")
    print(part2(input_lines))
