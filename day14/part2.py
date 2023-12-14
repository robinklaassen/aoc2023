from itertools import pairwise

from utils import read_input

type Point = tuple[int, int]


class RockyGrid:

    def __init__(self):
        self.xsize: int = 0
        self.ysize: int = 0
        self.blocks: list[Point] = []
        self.rounds: list[Point] = []
        self.num_rounds: int = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> 'RockyGrid':
        grid = RockyGrid()
        grid.ysize = len(lines)
        grid.xsize = len(lines[0])

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "O":
                    grid.rounds.append((x, y))
                elif char == "#":
                    grid.blocks.append((x, y))

        grid.num_rounds = len(grid.rounds)

        return grid

    def shift_rounds(self, direction: str = "north") -> None:
        all_new_rounds = []

        if direction in ["north", "south"]:
            for col_idx in range(self.xsize):
                round_ys = [y for x, y in self.rounds if x == col_idx]
                blocks_ys = [y for x, y in self.blocks if x == col_idx]

                for b1, b2 in pairwise([-1] + sorted(blocks_ys) + [self.ysize]):
                    num_rounds = sum(1 for y in round_ys if b1 < y < b2)
                    if direction == "north":
                        new_rounds = [(col_idx, b1 + offset + 1) for offset in range(num_rounds)]
                    elif direction == "south":
                        new_rounds = [(col_idx, b2 - offset - 1) for offset in range(num_rounds)]
                    all_new_rounds.extend(new_rounds)

        elif direction in ["east", "west"]:
            for row_idx in range(self.ysize):
                round_xs = [x for x, y in self.rounds if y == row_idx]
                blocks_xs = [x for x, y in self.blocks if y == row_idx]

                for b1, b2 in pairwise([-1] + sorted(blocks_xs) + [self.xsize]):
                    num_rounds = sum(1 for x in round_xs if b1 < x < b2)
                    if direction == "west":
                        new_rounds = [(b1 + offset + 1, row_idx) for offset in range(num_rounds)]
                    elif direction == "east":
                        new_rounds = [(b2 - offset - 1, row_idx) for offset in range(num_rounds)]
                    all_new_rounds.extend(new_rounds)

        else:
            raise ValueError()

        assert len(all_new_rounds) == self.num_rounds

        self.rounds = all_new_rounds

    def cycle(self, print_: bool = False) -> None:
        for direction in ["north", "west", "south", "east"]:
            self.shift_rounds(direction)
            if print_:
                print(f"After tilting {direction}:")
                self.print()
                print("")
        print(f"Score after cycle: {self.total_load_north()}")

    def total_load_north(self) -> int:
        return sum(self.ysize - y for (x, y) in self.rounds)

    def print(self):
        for y in range(self.ysize):
            line = ""
            for x in range(self.xsize):
                if (x, y) in self.blocks:
                    char = "#"
                elif (x, y) in self.rounds:
                    char = "O"
                else:
                    char = "."
                line += char
            print(line)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    test_grid = RockyGrid.from_lines(test_lines)
    test_grid.shift_rounds("north")
    assert test_grid.total_load_north() == 136

    input_lines = read_input("input.txt")
    grid = RockyGrid.from_lines(input_lines)
    grid.shift_rounds("north")
    assert grid.total_load_north() == 105461  # answer part 1

    # part 2
    test_grid = RockyGrid.from_lines(test_lines)
    # test_grid.cycle_until_steady(print_=False)
    # for _ in range(1000000000):
    #     test_grid.cycle()

    # There is a repeating pattern in cycle scores, it has length 7 for both test and input
    # I visually determined the start of the pattern then used modulus to determine score after 1e9 cycles :)

    grid = RockyGrid.from_lines(input_lines)
    for _ in range(10000000000):
        grid.cycle()
