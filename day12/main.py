from functools import cache

from utils import read_input


@cache
def possible_configs(spring: str, groups: str) -> int:
    if groups == "":
        # only possible if entire spring is '.'
        return 1 if "#" not in spring else 0

    if all(char == "." for char in spring):
        # can't fit any group into only '.'
        return 0

    if spring.startswith("."):
        # leading '.' are not relevant
        return possible_configs(spring.lstrip("."), groups)

    part_size = spring.index(".") if "." in spring else len(spring)  # first part of the spring with only #?
    target_size = int(groups.split(",")[0])

    if target_size > part_size:
        # skip to a new part of the spring
        return possible_configs(spring[part_size:], groups)

    next_groups = ",".join(groups.split(",")[1:]) if "," in groups else ""

    # this bit could be added into the loop below
    if target_size == part_size:
        # +1 because you need an extra . for separation
        return possible_configs(spring[target_size + 1:], next_groups)

    # multiple ways to put the part in target (exactly diff(sizes) + 1 times)
    total = 0
    for offset in range(part_size - target_size + 1):
        # can't be a # on the left side
        if offset != 0 and spring[offset - 1] == "#":
            continue

        # can't be a # on the right side
        if offset != (part_size - target_size) and spring[offset + target_size] == "#":
            continue

        total += possible_configs(spring[offset + target_size + 1:], next_groups)

    return total


# def possible_configs_extended(line: str) -> int:
#     spring, valid_str = line.split(" ")
#     spring_ext = "?".join([spring] * 5)
#     valid_str_ext = ",".join([valid_str] * 5)
#     validation_ext = [int(i) for i in valid_str_ext.split(",")]


def part1(lines: list[str]) -> int:
    return sum(possible_configs(*line.split(" ")) for line in lines)


# def part2(lines: list[str]) -> int:
#     total = 0
#     for idx, line in enumerate(lines):
#         print(f"{idx} / {len(lines)}")
#         total += possible_configs_extended(line)
#     return total


if __name__ == "__main__":

    assert possible_configs("???", "") == 1

    assert possible_configs("????", "1") == 4

    assert possible_configs("###", "3") == 1

    assert possible_configs("...", "3") == 0

    assert possible_configs("#?#?#", "") == 0

    assert possible_configs("???.###", "1,1,3") == 1

    assert possible_configs(".??..??...?##.", "1,1,3") == 4

    assert possible_configs("?###????????", "3,2,1") == 10

    test_lines = read_input("test_input.txt")
    expected = [1, 4, 1, 1, 4, 10]
    for idx, line in enumerate(test_lines):
        p = possible_configs(*line.split(" "))
        assert p == expected[idx]

    assert part1(test_lines) == 21

    input_lines = read_input("input.txt")
    for line in input_lines:
        print(possible_configs(*line.split(" ")))
    # print(part1(input_lines))  # 7191

    # part 2: bigger numbers, who would've thunk? can't brute force my way out of this probably
    # repeat the exercise with spring *= 5 and validation *= 5
    # assert part2(test_lines) == 525152
    # print(part2(input_lines))
