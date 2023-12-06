from math import sqrt, ceil, floor


def count_ways_to_win(time: int, distance: int) -> int:
    count = 0
    for charge_time in range(time + 1):
        travel_time = time - charge_time
        travel_distance = charge_time * travel_time
        if travel_distance > distance:
            count += 1

    return count


def do_smart(time: int, distance: int) -> int:
    # quadratic formula time babyyy
    intersect1 = (time + sqrt(time ** 2 - 4 * distance)) / 2
    intersect2 = (time - sqrt(time ** 2 - 4 * distance)) / 2

    return floor(intersect1) - ceil(intersect2) + 1


if __name__ == "__main__":
    assert count_ways_to_win(7, 9) == 4

    # For once, it was actually easier to just type the input here than make a parsing function :)
    times = [47, 84, 74, 67]
    distances = [207, 1394, 1209, 1014]

    output = 1
    for time, distance in zip(times, distances):
        ways = count_ways_to_win(time, distance)
        output *= ways
    print(f"Answer part 1: {output}")

    # part 2: look at me, I'm the big number now
    assert do_smart(71530, 940200) == 71503

    print(f"Answer part 2: {do_smart(47847467, 207139412091014)}")
