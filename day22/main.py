from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property, cache

from utils import read_input

type Loc = tuple[int, int, int]


# type Brick = tuple[Loc, Loc]


@dataclass
class Brick:
    id: int
    c1: Loc
    c2: Loc

    @property
    def xs(self) -> list[int]:
        return list(range(self.c1[0], self.c2[0] + 1))

    @property
    def ys(self) -> list[int]:
        return list(range(self.c1[1], self.c2[1] + 1))

    @property
    def zs(self) -> list[int]:
        return list(range(self.c1[2], self.c2[2] + 1))

    @property
    def height(self) -> int:
        return min(self.c1[2], self.c2[2])

    @property
    def positions(self) -> list[Loc]:
        return [
            (x, y, z)
            for x in self.xs
            for y in self.ys
            for z in self.zs
        ]

        # if self.c1[0] < self.c2[0]:
        #     return [(x, self.c1[1], self.c1[2]) for x in range(self.c1[0], self.c2[0] + 1)]
        # elif self.c1[1] < self.c2[1]:
        #     return [(self.c1[0], y, self.c1[2]) for y in range(self.c1[1], self.c2[1] + 1)]
        # elif self.c1[2] < self.c2[2]:
        #     return [(self.c1[0], self.c1[1], z) for z in range(self.c1[2], self.c2[2] + 1)]
        # else:
        #     return [self.c1]

    @property
    def lowest_positions(self) -> list[Loc]:
        return [p for p in self.positions if p[2] == self.height]

    def fall_to_height(self, height: int):
        diff = self.height - height
        assert diff >= 0
        self.c1 = (self.c1[0], self.c1[1], self.c1[2] - diff)
        self.c2 = (self.c2[0], self.c2[1], self.c2[2] - diff)

    def __hash__(self) -> int:
        return self.id


class Tetris:
    def __init__(self, lines: list[str]):
        self.bricks: list[Brick] = []
        for idx, line in enumerate(lines):
            loc1, loc2 = line.split("~")
            loc1 = tuple(int(x) for x in loc1.split(","))
            loc2 = tuple(int(x) for x in loc2.split(","))
            self.bricks.append(Brick(idx + 1, loc1, loc2))  # type: ignore

    @cached_property
    def positions(self) -> list[Loc]:
        return [pos for b in self.bricks for pos in b.positions]

    def settle(self):
        for brick in sorted(self.bricks, key=lambda b: b.height):
            # determine bricks directly below this one
            lower_bricks = [
                b
                for b in self.bricks
                if b != brick
                   and any(x in b.xs for x in brick.xs)
                   and any(y in b.ys for y in brick.ys)
                   and b.height < brick.height
            ]

            support_height = 0 if not lower_bricks else max(max(b.zs) for b in lower_bricks)
            brick.fall_to_height(support_height + 1)

        for brick in self.bricks:
            print(brick)

    def is_supported(self, brick: Brick, exclude: Brick | None = None) -> bool:
        for x in brick.xs:
            for y in brick.ys:
                z = brick.height - 1
                if z == 0:
                    return True  # supported by ground
                if (x, y, z) in exclude.positions:
                    continue
                if (x, y, z) in self.positions:
                    return True  # supported by another block
        return False


def part1(lines: list[str]) -> int:
    tetris = Tetris(lines)
    tetris.settle()

    # this performs horribly, but it runs in less than a few minutes, so...
    count = 0
    for b in tetris.bricks:
        if all(tetris.is_supported(br, exclude=b) for br in tetris.bricks):
            count += 1

    return count


def part2(lines: list[str]) -> int:
    tetris = Tetris(lines)
    tetris.settle()

    pos_to_id = {}
    for brick in tetris.bricks:
        for pos in brick.positions:
            pos_to_id[pos] = brick.id

    print(pos_to_id)

    supports = defaultdict(set)
    supported_by = defaultdict(set)
    for brick in tetris.bricks:
        for x in brick.xs:
            for y in brick.ys:
                upper_z = max(brick.zs)
                supported_id = pos_to_id.get((x, y, upper_z + 1), None)
                if supported_id is not None:
                    supports[brick.id].add(supported_id)

                lower_z = min(brick.zs)
                supported_by_id = pos_to_id.get((x, y, lower_z - 1), None)
                if supported_by_id is not None:
                    supported_by[brick.id].add(supported_by_id)

    print(supports)
    print(supported_by)

    # @cache
    def fallen_bricks(removed_brick_ids: set[int]) -> set[int]:
        output = set()
        if not removed_brick_ids:
            return output

        # supported_brick_ids = {br for rbr in removed_brick_ids for br in supports[rbr]}
        supported_brick_ids = set()
        for rem_br_id in removed_brick_ids:
            supported_brick_ids = supported_brick_ids.union(supports[rem_br_id])

        for supported_brick_id in supported_brick_ids:
            if len(supported_by[supported_brick_id].difference(removed_brick_ids)) > 0:
                # supported brick does not fall
                continue
            output.add(supported_brick_id)

        output = output.union(fallen_bricks(output))
        return output

    for br in tetris.bricks:
        print(f"{br.id} --> {fallen_bricks({br.id})}")

    return sum(len(fallen_bricks({br.id})) for br in tetris.bricks)


if __name__ == "__main__":
    test_lines = read_input("test.txt")
    # assert part1(test_lines) == 5

    input_lines = read_input("input.txt")
    # print(part1(input_lines))

    assert part2(test_lines) == 7
    print(part2(input_lines))  # 61140 too low
