import math

from utils import read_input


# god I hate graphs
# so... I won't :)

def parse_input(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    network = {}
    for line in lines:
        if not line:
            continue
        if not "=" in line:
            directions = line
            continue

        source, target = line.split(" = ")
        t1, t2 = target.split(", ")
        network[source] = (t1[1:], t2[:3])

    return directions, network


def count_steps(directions: str, network: dict[str, tuple[str, str]], start_location: str = "AAA") -> int:
    location = start_location
    steps = 0
    while not location.endswith("Z"):
        turn = directions[steps % len(directions)]
        location = network[location][0 if turn == "L" else 1]
        steps += 1

    return steps


def part1(lines: list[str]) -> int:
    directions, network = parse_input(lines)

    return count_steps(directions, network)


def part2(lines: list[str]) -> int:
    directions, network = parse_input(lines)

    # This is the fun part. Simultaneously counting steps will not perform.
    # Counting steps per start location will, however. And then it just repeats. So...
    step_counts = [count_steps(directions, network, start_loc) for start_loc in network if start_loc.endswith("A")]
    return math.lcm(*step_counts)  # least common multiple babyyy


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 6

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    print(part2(input_lines))
