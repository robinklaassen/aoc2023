from itertools import pairwise

from utils import read_input


def extrapolate_line(line: str) -> int:
    seq = [int(num) for num in line.split(" ")]

    all_seqs = [seq]

    while not all(num == 0 for num in all_seqs[-1]):
        all_seqs.append([i2 - i1 for i1, i2 in pairwise(all_seqs[-1])])

    last_numbers = [seq[-1] for seq in all_seqs]

    return sum(last_numbers)


def extrapolate_line_backwards(line: str) -> int:
    # Not very DRY, I know. Because it's an oasis!
    seq = [int(num) for num in line.split(" ")]

    all_seqs = [seq]

    while not all(num == 0 for num in all_seqs[-1]):
        all_seqs.append([i2 - i1 for i1, i2 in pairwise(all_seqs[-1])])

    first_numbers = [seq[0] for seq in all_seqs]

    # Trick of the alternating signs
    output = 0
    for idx, num in enumerate(first_numbers):
        output += num * (1 if idx % 2 == 0 else -1)

    return output


def part1(lines: list[str]) -> int:
    return sum(extrapolate_line(line) for line in lines)


def part2(lines: list[str]) -> int:
    return sum(extrapolate_line_backwards(line) for line in lines)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 114

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    assert part2(test_lines) == 2
    print(part2(input_lines))
