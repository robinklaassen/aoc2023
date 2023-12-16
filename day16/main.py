from queue import SimpleQueue
from typing import Literal

from utils import read_input

type Point = tuple[int, int]
type Direction = Literal["N", "S", "E", "W"]
type Beam = tuple[Point, Direction]


class Contraption:

    def __init__(self, lines: list[str]):
        self.xsize = len(lines[0])
        self.ysize = len(lines)

        self.energized_tiles: set[Point] = set()

        self.grid: dict[Point, str] = {}
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                self.grid[(x, y)] = char

    def reset(self):
        self.energized_tiles = set()

    def shift(self, point: Point, direction: Direction) -> Point:
        x, y = point
        return {
            "N": (x, y - 1),
            "S": (x, y + 1),
            "E": (x + 1, y),
            "W": (x - 1, y),
        }[direction]

    def on_grid(self, point: Point) -> bool:
        x, y = point
        return (0 <= x < self.xsize) and (0 <= y < self.ysize)

    def start_beam(self, start_beam: Beam = ((0, 0), "E")):
        queue = SimpleQueue()
        queue.put(start_beam)

        past_beams = set()

        while not queue.empty():
            beam: Beam = queue.get()
            if beam in past_beams:
                # The big stinker: beams loop on themselves! Ain't nobody got time for that.
                continue

            past_beams.add(beam)

            point, direction = beam
            if not self.on_grid(point):
                continue

            self.energized_tiles.add(point)

            next_beams = self.get_next_beams(beam)
            # print(f"{beam} ==> {next_beams}")

            for b in next_beams:
                queue.put(b)

    def get_next_beams(self, beam: Beam) -> list[Beam]:
        point, direction = beam

        match self.grid[point]:
            case ".":
                new_point = self.shift(point, direction)
                return [(new_point, direction)]
            case "\\":
                new_direction = {
                    "E": "S",
                    "S": "E",
                    "N": "W",
                    "W": "N",
                }[direction]
                new_point = self.shift(point, new_direction)
                return [(new_point, new_direction)]
            case "/":
                new_direction = {
                    "E": "N",
                    "N": "E",
                    "S": "W",
                    "W": "S",
                }[direction]
                new_point = self.shift(point, new_direction)
                return [(new_point, new_direction)]
            case "|":
                if direction in ["N", "S"]:
                    # continue as normal
                    new_point = self.shift(point, direction)
                    return [(new_point, direction)]
                else:
                    # split into N and S beams
                    new_directions: list[Direction] = ["N", "S"]
                    new_points = [self.shift(point, direction) for direction in new_directions]
                    return list(zip(new_points, new_directions))
            case "-":
                if direction in ["E", "W"]:
                    # continue as normal
                    new_point = self.shift(point, direction)
                    return [(new_point, direction)]
                else:
                    # split into E and W beams
                    new_directions: list[Direction] = ["E", "W"]
                    new_points = [self.shift(point, direction) for direction in new_directions]
                    return list(zip(new_points, new_directions))
            case _:
                raise ValueError("Should not happen")

    def find_best_config(self) -> int:
        beams: list[Beam] = []
        beams.extend(((x, 0), "S") for x in range(self.xsize))
        beams.extend(((x, self.ysize - 1), "N") for x in range(self.xsize))
        beams.extend(((0, y), "E") for y in range(self.ysize))
        beams.extend(((self.xsize - 1, y), "W") for y in range(self.ysize))

        scores: list[int] = []
        for beam in beams:
            self.reset()
            self.start_beam(beam)
            scores.append(len(self.energized_tiles))

        return max(scores)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    test_contraption = Contraption(test_lines)
    test_contraption.start_beam()
    assert len(test_contraption.energized_tiles) == 46

    input_lines = read_input("input.txt")
    contraption = Contraption(input_lines)
    contraption.start_beam()
    print(len(contraption.energized_tiles))

    # part 2
    assert test_contraption.find_best_config() == 51
    print(contraption.find_best_config())
