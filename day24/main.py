from dataclasses import dataclass
from itertools import combinations

from utils import read_input


@dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    @classmethod
    def from_line(cls, line: str) -> "Hailstone":
        line = line.replace(" @ ", ", ")
        args = [int(c) for c in line.split(", ")]
        return cls(*args)

    @property
    def path_params(self) -> tuple[float, float]:
        # y = ax + b, find a and b
        return self.vy / self.vx, self.py - (self.vy * self.px / self.vx)

    def intersect_xy(self, other: "Hailstone") -> tuple[float, float] | None:
        a1, b1 = self.path_params
        a2, b2 = other.path_params

        if a1 == a2:
            # parallel paths never cross
            return None

        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

        # check if t > 0 for both
        t1 = (x - self.px) / self.vx
        t2 = (x - other.px) / other.vx

        if t1 < 0 or t2 < 0:
            # crossed in the past
            return None

        return x, y


def part1(lines: list[str], min_intersect: int, max_intersect: int) -> int:
    hailstones = [Hailstone.from_line(line) for line in lines]
    count = 0
    for h1, h2 in combinations(hailstones, 2):
        intersect = h1.intersect_xy(h2)
        if intersect is not None:
            if all(min_intersect <= i <= max_intersect for i in intersect):
                count += 1
    return count


if __name__ == "__main__":
    test_lines = read_input("test.txt")
    assert part1(test_lines, 7, 27) == 2

    input_lines = read_input("input.txt")
    print(part1(input_lines, 200000000000000, 400000000000000))
