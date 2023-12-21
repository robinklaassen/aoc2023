from copy import copy
from dataclasses import dataclass

from utils import read_input, generate_grids


@dataclass(frozen=True)
class Part:
    props: dict[str, int]

    @classmethod
    def from_line(cls, line: str) -> "Part":
        line = line.strip("{}")
        props = {}
        for p in line.split(","):
            k, v = p.split("=")
            props[k] = int(v)
        assert all(c in props for c in "xmas")
        return cls(props)

    @property
    def total_rating(self) -> int:
        return sum(v for k, v in self.props.items() if k in "xmas")


@dataclass
class PartsRange:
    props: dict[str, tuple[int, int]]

    @classmethod
    def from_bounds(cls, lower_bounds: dict[str, int], upper_bounds: dict[str]) -> "PartsRange":
        props = {
            k: (lower_bounds[k], upper_bounds[k]) for k in "xmas"
        }
        return cls(props)

    def combinations(self) -> int:
        combinations = 1
        for rng in self.props.values():
            assert rng[1] > rng[0]
            combinations *= (rng[1] - rng[0])
        return combinations


@dataclass
class WorkflowSet:
    workflows: dict[str, str]

    @classmethod
    def from_lines(cls, lines: list[str]) -> "WorkflowSet":
        output = {}
        for line in lines:
            line = line.rstrip("}")
            k, v = line.split("{")
            output[k] = v
        return cls(output)

    def handle(self, part: Part) -> bool:
        flow_name = "in"

        while True:
            result = self.process_single_flow(flow_name, part)
            if result == "A":
                return True
            elif result == "R":
                return False
            else:
                flow_name = result

    def process_single_flow(self, flow_name: str, part: Part) -> str:
        workflow = self.workflows[flow_name]
        for step in workflow.split(","):
            if ">" in step:
                check, target = step.split(":")
                prop, num = check.split(">")
                if part.props[prop] > int(num):
                    return target
                else:
                    continue

            if "<" in step:
                check, target = step.split(":")
                prop, num = check.split("<")
                if part.props[prop] < int(num):
                    return target
                else:
                    continue

            return step

    def accepted_combinations(
            self, flow_name: str, lower_bounds: dict[str, int], upper_bounds: dict[str, int]
    ) -> list[PartsRange]:
        """
        Recursive function to find accepted combinations for a workflow with a given parts range.
        Should return a list of accepted ranges. Rejected ranges are void.
        """
        output_ranges = []

        workflow = self.workflows[flow_name]
        for step in workflow.split(","):
            if step == "A":
                output_ranges.append(PartsRange.from_bounds(lower_bounds, upper_bounds))
                return output_ranges
            elif step == "R":
                return output_ranges
            elif ":" not in step:
                output_ranges.extend(self.accepted_combinations(step, lower_bounds, upper_bounds))
                return output_ranges

            # now, there is always a condition in this step
            check, target = step.split(":")

            if ">" in step:
                prop, num = check.split(">")

                # accepted for target
                new_lower = copy(lower_bounds)
                new_lower[prop] = max(new_lower[prop], int(num) + 1)
                new_upper = copy(upper_bounds)

                if target == "A":
                    output_ranges.append(PartsRange.from_bounds(new_lower, new_upper))
                elif target != "R":
                    output_ranges.extend(self.accepted_combinations(target, new_lower, new_upper))
                else:
                    # rejected, do nothing
                    pass

                # passing to next step
                upper_bounds[prop] = min(upper_bounds[prop], int(num) + 1)
            elif "<" in step:
                prop, num = check.split("<")

                # accepted for target
                new_lower = copy(lower_bounds)
                new_upper = copy(upper_bounds)
                new_upper[prop] = min(new_upper[prop], int(num))

                if target == "A":
                    output_ranges.append(PartsRange.from_bounds(new_lower, new_upper))
                elif target != "R":
                    output_ranges.extend(self.accepted_combinations(target, new_lower, new_upper))
                else:
                    # rejected, do nothing
                    pass

                # passing to next step
                lower_bounds[prop] = max(lower_bounds[prop], int(num))


def part1(lines: list[str]) -> int:
    workflows, parts = tuple(generate_grids(lines))
    workflow_set = WorkflowSet.from_lines(workflows)
    parts = [Part.from_line(line) for line in parts]

    return sum(p.total_rating for p in parts if workflow_set.handle(p))


def part2(lines: list[str]) -> int:
    workflows, parts = tuple(generate_grids(lines))
    workflow_set = WorkflowSet.from_lines(workflows)

    lower_bounds = {k: 1 for k in "xmas"}
    upper_bounds = {k: 4001 for k in "xmas"}

    parts_ranges = workflow_set.accepted_combinations("in", lower_bounds, upper_bounds)

    return sum(pr.combinations() for pr in parts_ranges)


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 19114

    input_lines = read_input("input.txt")
    print(part1(input_lines))

    assert part2(test_lines) == 167409079868000
    print(part2(input_lines))
