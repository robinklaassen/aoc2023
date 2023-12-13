from utils import read_input


def possible_configs(spring: str, groups: str) -> int:
    if groups == "":
        # only possible if entire spring is '.'
        return 1 if "#" not in spring else 0

    if "?" not in spring:
        spring_groups = [len(g) for g in spring.split(".") if g]
        return 1 if spring_groups == [int(g) for g in groups.split(",")] else 0

    idx = spring.index("?")

    new_springs = [spring[:idx] + c + spring[idx + 1:] for c in ".#"]
    return sum(possible_configs(spr, groups) for spr in new_springs)


def part1(lines: list[str]) -> int:
    return sum(possible_configs(*line.split(" ")) for line in lines)


if __name__ == "__main__":
    assert possible_configs("?", "3") == 0

    assert possible_configs("???", "") == 1

    assert possible_configs("???", "1,1") == 1

    assert possible_configs("????", "1") == 4

    assert possible_configs("?.?.??", "1,2") == 2

    assert possible_configs("###", "3") == 1

    assert possible_configs("...", "3") == 0

    assert possible_configs("#?#?#", "") == 0

    assert possible_configs("???.###", "1,1,3") == 1

    assert possible_configs(".??..??...?##.", "1,1,3") == 4

    assert possible_configs("?###????????", "3,2,1") == 10

    assert possible_configs("??#??????#???.?", "4,3") == 9

    assert possible_configs("?.?..?..?????", "1,4") == 6

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

    # brute forcing doesn't work for part 2...