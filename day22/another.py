# I basically redid the entire thing from scratch to check my thinking
from dataclasses import dataclass

from utils import read_input

type Pos = tuple[int, int, int]


@dataclass
class Brick:
    id: int
    positions: list[Pos]

    @classmethod
    def from_line(cls, idx: int, line: str) -> "Brick":
        str1, str2 = line.split("~")
        pos1 = tuple(int(c) for c in str1.split(","))
        pos2 = tuple(int(c) for c in str2.split(","))
        orientation_idx = next((i for i in range(3) if pos1[i] != pos2[i]), None)

        if orientation_idx is None:
            return cls(idx + 1, [pos1])

        all_pos = []
        for d in range(pos1[orientation_idx], pos2[orientation_idx] + 1):
            pos = list(pos1)
            pos[orientation_idx] = d
            all_pos.append(tuple(pos))

        return cls(idx + 1, all_pos)

    @property
    def xy(self) -> set[tuple[int, int]]:
        return set((x, y) for x in self.coords(0) for y in self.coords(1))

    @property
    def lowest_z(self) -> int:
        return min(self.coords(2))

    @property
    def highest_z(self) -> int:
        return max(self.coords(2))

    def coords(self, idx: int) -> list[int]:
        return [p[idx] for p in self.positions]

    def fall_to(self, target_z: int):
        diff = self.lowest_z - target_z
        self.positions = [(x, y, z - diff) for x, y, z in self.positions]


def settle(bricks: list[Brick]) -> None:  # in place
    for brick in sorted(bricks, key=lambda b: b.lowest_z):  # loop, starting with lowest bricks first
        lower_bricks = [b for b in bricks if len(b.xy.intersection(brick.xy)) > 0 and b.lowest_z < brick.lowest_z]
        target_z = max(b.highest_z for b in lower_bricks) + 1 if lower_bricks else 1
        brick.fall_to(target_z)


def count_fallen(supports, supported_by, removed_ids: set[int]) -> int:
    # determine blocks that possibly COULD BE falling now
    targets = set()
    for rid in removed_ids:
        targets.update(supports[rid])

    targets.difference_update(removed_ids)  # don't re-check already falling blocks

    # determine blocks that are actually falling
    fallen = set()
    for t in targets:
        if len(supported_by[t] - removed_ids) == 0:
            fallen.add(t)

    if not fallen:
        return 0
    else:
        return len(fallen) + count_fallen(supports, supported_by, removed_ids.union(fallen))


def both_parts(lines: list[str]) -> tuple[int, int]:
    bricks = [Brick.from_line(idx, line) for idx, line in enumerate(lines)]
    settle(bricks)

    posmap: dict[Pos, int] = {pos: b.id for b in bricks for pos in b.positions}

    supports: dict[int, set[int]] = {}
    supported_by: dict[int, set[int]] = {}
    for brick in bricks:
        print(brick)
        supports[brick.id] = set()
        supported_by[brick.id] = set()

        for x in brick.coords(0):
            for y in brick.coords(1):
                pos_above = (x, y, brick.highest_z + 1)
                if pos_above in posmap:
                    supports[brick.id].add(posmap[pos_above])

                pos_below = (x, y, brick.lowest_z - 1)
                if pos_below in posmap:
                    supported_by[brick.id].add(posmap[pos_below])
                elif brick.lowest_z == 1:
                    supported_by[brick.id].add(0)  # ground

    print(supports)
    print(supported_by)

    # all bricks should be supported by something, otherwise the stack has not settled properly
    assert all(len(v) > 0 for v in supported_by.values())

    fall_count = {b.id: count_fallen(supports, supported_by, {b.id}) for b in bricks}
    print(fall_count)

    safely_disintegrate_count = sum(1 for v in fall_count.values() if v == 0)
    chain_total = sum(v for v in fall_count.values())
    return safely_disintegrate_count, chain_total


if __name__ == "__main__":
    test_lines = read_input("test.txt")
    assert both_parts(test_lines) == (5, 7)

    input_lines = read_input("input.txt")
    print(both_parts(input_lines))
