from utils import read_input


def config_is_valid(config: str, validation: list[int]) -> bool:
    assert "?" not in config
    return [len(x) for x in config.split(".") if x] == validation


def possible_configs(line: str) -> int:
    spring, valid_str = line.split(" ")
    validation = [int(i) for i in valid_str.split(",")]

    return sum(1 for conf in generate_configs(spring) if config_is_valid(conf, validation))


def generate_configs(spring: str) -> list[str]:
    configs: list[str] = [""]
    for char in spring:
        if char == "?":
            configs = [s + "#" for s in configs] + [s + "." for s in configs]
        else:
            configs = [s + char for s in configs]

    return configs


def part1(lines: list[str]) -> int:
    return sum(possible_configs(line) for line in lines)


if __name__ == "__main__":
    assert config_is_valid("#.#.###", [1, 1, 3])

    assert possible_configs("???.### 1,1,3") == 1

    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 21

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    # part 2: bigger numbers, who would've thunk? can't brute force my way out of this probably
    # repeat the exercise with spring *= 5 and validation *= 5
    pass
