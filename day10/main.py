from utils import read_input


def shift(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    x, y = pos
    shifts = {
        "north": (x, y - 1),
        "south": (x, y + 1),
        "east": (x + 1, y),
        "west": (x - 1, y),
    }
    return shifts[direction]


def reverse(direction: str) -> str:
    return {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
    }[direction]


def connections(char: str) -> list[str]:
    match char:
        case "|":
            return ["north", "south"]
        case "-":
            return ["east", "west"]
        case "L":
            return ["north", "east"]
        case "J":
            return ["north", "west"]
        case "7":
            return ["south", "west"]
        case "F":
            return ["south", "east"]
        case _:
            return []


def get_loop_nodes(lines: list[str]) -> list[tuple[int, int]]:
    # note: starting node is included 2 times
    start_node = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start_node = x, y
                break

    assert start_node is not None

    for direction in ["east", "west", "north", "south"]:
        pos = start_node
        path_nodes = [pos]
        try:
            while True:
                new_pos = shift(pos, direction)
                new_x, new_y = new_pos
                new_char = lines[new_y][new_x]
                if new_char == "S":
                    path_nodes.append(new_pos)
                    return path_nodes

                if reverse(direction) not in connections(new_char):
                    raise Exception("Traversal error")

                pos = new_pos
                path_nodes.append(pos)
                direction = next(d for d in connections(new_char) if d != reverse(direction))

        except Exception:
            pass


def part1(lines: list[str]) -> int:
    path_nodes = get_loop_nodes(lines)
    return int(len(path_nodes) / 2)


def part2(lines: list[str]) -> int:
    print("---part2---")
    path_nodes = get_loop_nodes(lines)

    # determine what S should be
    start_node = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                start_node = x, y
                break

    assert start_node is not None

    x, y = start_node

    connected_directions = []
    for d in ["north", "east", "south", "west"]:
        new_pos = shift(start_node, d)
        new_x, new_y = new_pos
        new_char = lines[new_y][new_x]
        if reverse(d) in connections(new_char):
            connected_directions.append(d)

    char = next(c for c in "LJF7|-" if set(connections(c)) == set(connected_directions))
    lines[y] = lines[y].replace("S", char)

    # now the inner/outer magic happens
    count = 0
    for y, line in enumerate(lines):
        inside = False
        last_bend = None
        visual_line = []
        for x, char in enumerate(line):
            pos = x, y

            if pos not in path_nodes:
                count += (1 if inside else 0)
                visual_line.append("I" if inside else "O")
                continue

            visual_line.append("P")

            if char == "|":
                inside = not inside

            if char in ["F", "7"]:  # south bending
                if last_bend == "north":
                    inside = not inside
                    last_bend = None
                elif last_bend == "south":
                    last_bend = None
                elif last_bend is None:
                    last_bend = "south"
                else:
                    raise Exception("wtf")

            if char in ["L", "J"]:  # north bending
                if last_bend == "south":
                    inside = not inside
                    last_bend = None
                elif last_bend == "north":
                    last_bend = None
                elif last_bend is None:
                    last_bend = "north"
                else:
                    raise Exception("wtf")

        print("".join(visual_line))  # much needed for debugging

    return count


if __name__ == "__main__":
    test_lines_1 = read_input("test_input1.txt")
    assert part1(test_lines_1) == 4

    test_lines_2 = read_input("test_input2.txt")
    assert part1(test_lines_2) == 8

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    assert part2(test_lines_1) == 1
    assert part2(test_lines_2) == 1

    print(part2(input_lines))
