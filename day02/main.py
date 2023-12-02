from utils import read_input

input_lines = read_input("input.txt")

valid_game_ids = []

BAG_CUBE_COUNT = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def validate_game_line(cubes: str) -> bool:
    cube_sets = cubes.split("; ")
    for cube_set in cube_sets:
        cube_types = cube_set.split(", ")
        for cube_type in cube_types:
            count, color = cube_type.split(" ")
            if int(count) > BAG_CUBE_COUNT[color]:
                return False
    return True


for line in input_lines:
    game_tag, cubes = line.split(": ")
    game_id = int(game_tag.split(" ")[1])

    if validate_game_line(cubes):
        valid_game_ids.append(game_id)

print(valid_game_ids)
print(sum(valid_game_ids))

# part 2

game_powers = []


def generate_cube_counts(cubes: str):
    # part 1 could be refactored using this generator! But, who cares.
    cube_sets = cubes.split("; ")
    for cube_set in cube_sets:
        cube_types = cube_set.split(", ")
        for cube_type in cube_types:
            count, color = cube_type.split(" ")
            yield color, int(count)


for line in input_lines:
    game_tag, cubes = line.split(": ")
    game_id = int(game_tag.split(" ")[1])

    max_cube_count = {
        "red": 0,
        "blue": 0,
        "green": 0,
    }

    for cube_color, cube_count in generate_cube_counts(cubes):
        max_cube_count[cube_color] = max(max_cube_count[cube_color], cube_count)

    cube_power = max_cube_count["red"] * max_cube_count["blue"] * max_cube_count["green"]
    game_powers.append(cube_power)

print(game_powers)
print(sum(game_powers))
