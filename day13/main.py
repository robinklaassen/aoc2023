from utils import read_input, generate_grids


def find_any_reflection_line(pattern: list[str], exclude_score: int | None = None) -> int | None:
    # assumes one reflection per pattern

    if exclude_score is not None:
        exclude_horizontal_index = exclude_score / 100 if exclude_score >= 100 else -1
        exclude_vertical_index = exclude_score if exclude_score < 100 else -1
    else:
        exclude_horizontal_index = -1
        exclude_vertical_index = -1

    # horizontal
    if (idx := find_reflection_line(pattern, exclude_horizontal_index)) is not None:
        return 100 * idx

    # vertical
    rotated_pattern = ["".join(list(tup)) for tup in zip(*pattern)]
    if (idx := find_reflection_line(rotated_pattern, exclude_vertical_index)) is not None:
        return idx

    return None


def find_reflection_line(pattern: list[str], exclude_idx: int = -1) -> int | None:
    for i in range(1, len(pattern)):  # can't reflect above first line
        first_part = pattern[0:i]
        first_part.reverse()
        second_part = pattern[i:]

        check_size = min(len(first_part), len(second_part))
        if first_part[:check_size] == second_part[:check_size] and i != exclude_idx:
            return i
    return None


def find_smudged_reflection(pattern: list[str]) -> int:
    default_score = find_any_reflection_line(pattern)

    for y, line in enumerate(pattern):
        for x, char in enumerate(line):
            fixed_pattern = pattern.copy()
            new_char = "." if char == "#" else "#"
            fixed_pattern[y] = line[:x] + new_char + line[x + 1:]

            score = find_any_reflection_line(fixed_pattern, exclude_score=default_score)
            if score is not None:
                return score

    raise Exception("No smudged reflection found in pattern!")


def part1(lines: list[str]) -> int:
    return sum(find_any_reflection_line(p) for p in generate_grids(lines))


def part2(lines: list[str]) -> int:
    return sum(find_smudged_reflection(p) for p in generate_grids(lines))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 405

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    assert part2(test_lines) == 400
    print(part2(input_lines))
