import math
from collections import defaultdict
from dataclasses import dataclass
from queue import SimpleQueue

from utils import read_input

type Pulse = tuple[str, str, int]  # source, target, low/high pulse (0/1)


def get_line(lines: list[str], name: str) -> str | None:
    if name == "broadcaster":
        return next(line for line in lines if line.startswith("broadcaster"))

    return next((line for line in lines if not line.startswith("broadcaster") and name in line.split("->")[0]), None)


class Comms:

    def __init__(self, lines: list[str]):
        self.lines = lines

        self.flipflop_state: dict[str, bool] = defaultdict(lambda: False)
        self.conjunction_memory: dict[str, dict[str, int]] = {}
        self.queue = SimpleQueue()

        self.reset()

    def reset(self):
        self.flipflop_state: dict[str, bool] = defaultdict(lambda: False)
        self.conjunction_memory: dict[str, dict[str, int]] = {}

        # initialize conjunction memory with all inputs
        for line in self.lines:
            if line.startswith("&"):
                self.conjunction_memory[line.split(" -> ")[0]] = {}

        for line in self.lines:
            source = line.split(" -> ")[0]
            outputs = line.split(" -> ")[1].split(", ")
            for output in outputs:
                if "&" + output in self.conjunction_memory:
                    self.conjunction_memory["&" + output][source] = 0

    def push_button(self, break_on_high: str | None = None, break_on_low: str | None = None) -> tuple[int, int]:
        # The time has come to...
        # print("PUSH THE BUTTON")
        self.queue.put(("button", "broadcaster", 0))
        return self.run(break_on_high, break_on_low)

    def run(self, break_on_high: str | None = None, break_on_low: str | None = None) -> tuple[int, int]:
        pulse_counts = [0, 0]

        last_break_on_high: int | None = None

        while not self.queue.empty():
            pulse = self.queue.get()
            # print(pulse)
            source_name, target_name, pulse_type = pulse
            pulse_counts[pulse_type] += 1

            if break_on_high is not None and target_name == break_on_high:
                last_break_on_high = pulse_type

            # if break_on_high is not None and target_name == break_on_high and pulse_type == 1:
            #     return -1, -1

            if break_on_low is not None and target_name == break_on_low and pulse_type == 0:
                return -1, -1

            target_line = get_line(self.lines, target_name)
            if target_line is None:
                continue

            new_source = target_line.split(" -> ")[0]
            outputs = target_line.split(" -> ")[1].split(", ")

            if new_source == "broadcaster":
                # broadcaster
                new_pulse_type = pulse_type
            elif new_source.startswith("%"):
                # flip-flop
                if pulse_type == 1:
                    continue

                state = self.flipflop_state[new_source]
                new_state = not state
                self.flipflop_state[new_source] = new_state
                new_pulse_type = 1 if new_state else 0
            elif new_source.startswith("&"):
                # conjunction
                mem = self.conjunction_memory[new_source]
                mem[source_name] = pulse_type
                # if new_source == "&zp":
                #     print(mem)
                new_pulse_type = 0 if all(mem.values()) else 1
            else:
                raise ValueError("wtf")

            for output in outputs:
                self.queue.put((new_source, output, new_pulse_type))

        # check for targets

        if self.conjunction_memory["&zp"]["&" + break_on_high] == 1:
            return -1, -1

        # if last_break_on_high == 1:
        #     return -1, -1

        return pulse_counts[0], pulse_counts[1]


def part1(lines: list[str]) -> int:
    comms = Comms(lines)

    low_count, high_count = 0, 0

    for _ in range(1000):
        low, high = comms.push_button()
        # print(low, high)
        low_count += low
        high_count += high

    return low_count * high_count


def part2(lines: list[str]) -> int:
    comms = Comms(lines)

    # The below doesn't perform at all. Shocker!
    # presses = 0
    # while True:
    #     presses += 1
    #     if comms.push_button(break_on_low="rx") == (-1, -1):
    #         break
    #
    # return presses

    all_presses = {}
    for module in ["sb", "nd", "ds", "hf"]:
        comms.reset()
        presses = 0
        while True:
            presses += 1
            if comms.push_button(break_on_high=module) == (-1, -1):
                print(f"{presses} presses to reach high pulse on {module}")
                break
        all_presses[module] = presses

    return math.lcm(*all_presses.values())


if __name__ == "__main__":
    # test1_lines = read_input("test1.txt")
    # assert part1(test1_lines) == 32000000
    #
    # test2_lines = read_input("test2.txt")
    # assert part1(test2_lines) == 11687500
    #
    input_lines = read_input("input.txt")
    # print(part1(input_lines))

    print(part2(input_lines))
