import math
from collections import deque
from dataclasses import dataclass

import networkx as nx

from ipysigma import Sigma

from utils import read_input


@dataclass
class Network:
    flipflops: dict[str, bool]  # True = on
    conjunctions: dict[str, dict[str, int]]
    targets: dict[str, list[str]]

    queue = deque()
    counter: int = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Network":
        flipflops = {}
        conjunctions = {}
        targets = {}

        for line in lines:
            left, right = line.split(" -> ")
            module_name = left.lstrip("%&")
            outputs = right.split(", ")

            targets[module_name] = outputs

            if left.startswith("%"):
                flipflops[module_name] = False
            elif left.startswith("&"):
                conjunctions[module_name] = {}

        # run again to explicitly set conjunctions memory
        for line in lines:
            left, right = line.split(" -> ")
            module_name = left.lstrip("%&")
            outputs = right.split(", ")

            for output in outputs:
                if output in conjunctions:
                    conjunctions[output][module_name] = 0

        return cls(flipflops, conjunctions, targets)

    def push_button(self) -> tuple[int, int]:
        # print("--- PUSH BUTTON ---")
        assert len(self.queue) == 0
        self.counter += 1
        self.queue.append(("button", 0, "broadcaster"))
        return self.handle_queue()

    def handle_queue(self) -> tuple[int, int]:
        pulse_counts = {0: 0, 1: 0}
        while len(self.queue) > 0:
            source, in_pulse, module = self.queue.popleft()
            # print(f"{source} -{'high' if in_pulse else 'low'}-> {module}")
            pulse_counts[in_pulse] += 1

            if module not in self.targets:
                continue

            targets = self.targets[module]

            if module == "broadcaster":
                out_pulse = in_pulse
            elif module in self.flipflops:
                if in_pulse == 1:
                    continue
                self.flipflops[module] = not self.flipflops[module]
                out_pulse = 1 if self.flipflops[module] else 0
            elif module in self.conjunctions:
                mem = self.conjunctions[module]
                mem[source] = in_pulse
                out_pulse = 0 if all(mem.values()) else 1
            else:
                raise ValueError("wtf")

            for target in targets:
                self.queue.append((module, out_pulse, target))

            if module in ["vn", "nt", "vv", "zq"] and out_pulse == 0:
                # this is the input for LCM
                print(f"{module} sends low pulse after {self.counter} presses")

        return pulse_counts[0], pulse_counts[1]

    def to_graph(self) -> nx.DiGraph:
        graph = nx.DiGraph()
        for module in self.targets:
            for output in self.targets[module]:
                graph.add_edge(module, output)

        for module in graph:
            if module in self.flipflops:
                module_type = "flipflop"
            elif module in self.conjunctions:
                module_type = "conjunction"
            else:
                module_type = "other"
            graph.nodes[module]["type"] = module_type

        return graph


def part1(lines: list[str]) -> int:
    print("PART 1")
    network = Network.from_lines(lines)

    low_count = high_count = 0
    for _ in range(1000):
        low, high = network.push_button()
        low_count += low
        high_count += high

    return low_count * high_count


def part2(lines: list[str]) -> int:
    print("PART 2")
    network = Network.from_lines(lines)

    # Visualize the network to understand its workings :)
    # graph = network.to_graph()
    # sigma = Sigma(graph, height=1000, node_color="type")
    # sigma.to_html("graph.html")

    # inputs read from console, too lazy to change the code
    return math.lcm(3733, 3797, 3877, 3917)


if __name__ == "__main__":
    test1_lines = read_input("test1.txt")
    assert part1(test1_lines) == 32000000

    test2_lines = read_input("test2.txt")
    assert part1(test2_lines) == 11687500

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    print(part2(input_lines))
