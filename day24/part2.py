import z3

from utils import read_input


def solve(lines: list[str]) -> int:
    # never used this before. Now is as good a time as any.
    solver = z3.Solver()

    x, y, z, vx, vy, vz = z3.Reals("x y z vx vy vz")

    # we only need 3 hailstones. Since that produces 9 equations with 9 unknowns, it should be solvable.
    for idx, line in enumerate(lines[:3]):
        left, right = line.split(" @ ")
        hx, hy, hz = tuple(int(c) for c in left.split(", "))
        hvx, hvy, hvz = tuple(int(c) for c in right.split(", "))

        t = z3.Real(f"t{idx + 1}")

        solver.add(hx + hvx * t == x + vx * t)
        solver.add(hy + hvy * t == y + vy * t)
        solver.add(hz + hvz * t == z + vz * t)

    result = solver.check()
    assert str(result) == "sat"

    model = solver.model()
    added_coords = model.eval(x).as_long() + model.eval(y).as_long() + model.eval(z).as_long()
    return added_coords


if __name__ == "__main__":
    test_lines = read_input("test.txt")
    assert solve(test_lines) == 47

    input_lines = read_input("input.txt")
    print(solve(input_lines))
