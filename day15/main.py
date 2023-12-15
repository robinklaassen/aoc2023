from collections import defaultdict

from utils import read_input


def do_hash(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


def part1(string: str) -> int:
    return sum(do_hash(s) for s in string.split(","))


def part2(string: str) -> int:
    boxes: dict[int, list[tuple[str, int]]] = defaultdict(list)

    for s in string.split(","):
        if "-" in s:
            label = s.split("-")[0]
            idx = do_hash(label)

            target_lens = next((l for l in boxes[idx] if l[0] == label), None)
            if target_lens is not None:
                boxes[idx].remove(target_lens)

        elif "=" in s:
            label, value = s.split("=")
            value = int(value)
            idx = do_hash(label)

            target_lens = next((l for l in boxes[idx] if l[0] == label), None)
            if target_lens is not None:
                target_idx = boxes[idx].index(target_lens)
                boxes[idx][target_idx] = (label, value)
            else:
                boxes[idx].append((label, value))

        else:
            raise ValueError(f"Don't know what to do with `{s}`")

    # Focusing power
    power = 0

    for idx, lenses in boxes.items():
        for lens_idx, lens in enumerate(lenses):
            power += ((idx + 1) * (lens_idx + 1) * lens[1])

    return power


if __name__ == "__main__":
    assert do_hash("HASH") == 52

    test_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    assert part1(test_input) == 1320

    puzzle_input = read_input("input.txt")[0]
    print(part1(puzzle_input))

    assert part2(test_input) == 145
    print(part2(puzzle_input))
