# happy Sinterklaas!
from functools import cache

from utils import read_input


class RangeMap:
    def __init__(self):
        self.name: str = ""
        self.ranges: list[tuple[int, int, int]] = []

    @cache
    def convert(self, num_in: int) -> int:
        for dest_start, source_start, length in self.ranges:
            # example: 50 98 2. which means 98 and 99 map to 50 and 51
            diff = num_in - source_start
            if 0 <= diff < length:
                return dest_start + diff
        return num_in

    @cache
    def reverse(self, dest: int) -> int:
        for dest_start, source_start, length in self.ranges:
            diff = dest - dest_start
            if 0 <= diff < length:
                return source_start + diff
        return dest

    def __repr__(self):
        return self.name


def parse_input(lines: list[str]) -> tuple[list[int], list[RangeMap]]:
    range_maps = []
    range_map = None
    for line in lines:
        if line.startswith("seeds"):
            seeds = [int(s) for s in line.split(": ")[1].split(" ")]
            continue

        if not line:
            if range_map is not None:
                range_maps.append(range_map)
            continue

        if line[0].isalpha():
            range_map = RangeMap()
            range_map.name = line

        if line[0].isnumeric():
            range_map.ranges.append(tuple(int(n) for n in line.split(" ")))  # type: ignore

    range_maps.append(range_map)

    return seeds, range_maps


# @cache
def convert_seed(seed: int, range_maps: list[RangeMap]) -> int:
    value = seed
    for range_map in range_maps:
        value = range_map.convert(value)
    return value


def convert_seeds(seeds: list[int], range_maps: list[RangeMap]) -> list[int]:
    return [convert_seed(seed, range_maps) for seed in seeds]


def get_seed_for_location(location: int, range_maps: list[RangeMap]) -> int:
    value = location
    for range_map in reversed(range_maps):
        value = range_map.reverse(value)
    return value


def seed_in_given_ranges(seed: int, seed_ranges: list[int]) -> bool:
    for i in range(0, len(seed_ranges), 2):
        range_start = seed_ranges[i]
        range_length = seed_ranges[i + 1]
        diff = seed - range_start
        if 0 <= diff < range_length:
            return True
    return False


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    seeds, range_maps = parse_input(test_lines)
    values = convert_seeds(seeds, range_maps)
    print(values)
    assert min(values) == 35

    input_lines = read_input("input.txt")
    seeds, range_maps = parse_input(input_lines)
    values = convert_seeds(seeds, range_maps)
    print(values)
    print(min(values))

    # part 2, seeds are now ranges yay
    print("---PART 2---")
    location: int = 0
    while True:
        seed = get_seed_for_location(location, range_maps)
        if seed_in_given_ranges(seed, seed_ranges=seeds):
            break
        location += 1000

    location -= 1000
    while True:
        seed = get_seed_for_location(location, range_maps)
        if seed_in_given_ranges(seed, seed_ranges=seeds):
            break
        location += 1

    print(location)
