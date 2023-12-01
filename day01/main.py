from utils import read_input

import re

input_lines = read_input("input.txt")

calibration_values = []

for line in input_lines:
    digits = [char for char in line if char.isnumeric()]
    number = digits[0] + digits[-1]
    calibration_values.append(int(number))

print(sum(calibration_values))

# part 2

number_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

combo_number_map = {
    "oneight": "18",
    "threeight": "38",
    "fiveight": "58",
    "nineight": "98",
    "twone": "21",
    "sevenine": "79",
    "eightwo": "82",
    "eighthree": "83",
}


def parse_line(line: str) -> int:
    for in_, out_ in combo_number_map.items():
        line = line.replace(in_, out_)

    while True:
        result = re.search(r"(one|two|three|four|five|six|seven|eight|nine)", line)
        if result is None:
            break

        first_match = result.group(1)
        line = line.replace(first_match, number_map[first_match])

    digits = [char for char in line if char.isnumeric()]

    number = int(digits[0] + digits[-1])
    assert number >= 10
    assert number < 100
    return number


tests = {
    "two1nine": 29,
    "eightwothree": 83,  # eight should be replaced before two!!
    "abcone2threexyz": 13,
    "xtwone3four": 24,
    "4nineeightseven2": 42,
    "zoneight234": 14,
    "7pqrstsixteen": 76,
    "eighthree": 83,
}

for test_input, expected_result in tests.items():
    assert parse_line(test_input) == expected_result

calibration_values = [parse_line(line) for line in input_lines]
print(sum(calibration_values))
