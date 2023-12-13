from functools import cache

from utils import read_input


@cache  # dynamic programming babyyy
def possible_configs(spring: str, groups: str) -> int:
    if groups == "":
        # only possible if entire spring is '.'
        return 1 if "#" not in spring else 0

    if all(char == "." for char in spring):
        # can't fit any group into only '.'
        return 0

    target_size = int(groups.split(",")[0])
    next_groups = ",".join(groups.split(",")[1:]) if "," in groups else ""

    if target_size > len(spring):
        return 0

    total = 0
    for offset in range(len(spring) - target_size + 1):

        target = spring[offset:offset + target_size]
        if "." in target:
            continue

        # can't be a # on the left side ANYWHERE
        if "#" in spring[:offset]:
            continue

        # can't be a # directly on the right side
        if offset + target_size != len(spring) and spring[offset + target_size] == "#":
            continue

        next_spring = spring[offset + target_size + 1:]
        count = possible_configs(next_spring, next_groups)
        # print(f"{next_spring} --- {next_groups} --- {count}")
        total += count

    return total


def part1(lines: list[str]) -> int:
    return sum(possible_configs(*line.split(" ")) for line in lines)


def part2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        spring, groups = line.split(" ")
        extended_spring = "?".join([spring] * 5)
        extended_groups = ",".join([groups] * 5)
        total += possible_configs(extended_spring, extended_groups)
    return total


if __name__ == "__main__":
    # yes, I needed this many explicit test cases

    assert possible_configs("?", "3") == 0

    assert possible_configs("???", "") == 1

    assert possible_configs("????", "1") == 4

    assert possible_configs("???", "1,1") == 1

    assert possible_configs("????", "1,1") == 3

    assert possible_configs("?.?.??", "1,2") == 2

    assert possible_configs("###", "3") == 1

    assert possible_configs("...", "3") == 0

    assert possible_configs("#?#?#", "") == 0

    assert possible_configs("???.###", "1,1,3") == 1

    assert possible_configs(".??..??...?##.", "1,1,3") == 4

    assert possible_configs("?###????????", "3,2,1") == 10

    assert possible_configs("????#???.?", "3") == 3

    assert possible_configs("??#??????#???.?", "4,3") == 9  # now 10

    assert possible_configs("?.?..?..?????", "1,4") == 6

    assert possible_configs("?.#?", "1") == 1

    assert possible_configs("?#???..?.#?", "2,2,1") == 1

    assert possible_configs(".??#.?????..????#?.", "1,1,5") == 12  # now 46

    test_lines = read_input("test_input.txt")
    expected = [1, 4, 1, 1, 4, 10]
    for idx, line in enumerate(test_lines):
        p = possible_configs(*line.split(" "))
        assert p == expected[idx]

    assert part1(test_lines) == 21

    input_lines = read_input("input.txt")
    for line in input_lines:
        print(possible_configs(*line.split(" ")))

    print(part1(input_lines))

    # part 2: bigger numbers, who would've thunk?
    assert part2(test_lines) == 525152
    print(part2(input_lines))
