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


def part1(lines: list[str]):
    workflows, parts = tuple(generate_grids(lines))
    workflow_set = WorkflowSet.from_lines(workflows)
    parts = [Part.from_line(line) for line in parts]

    return sum(p.total_rating for p in parts if workflow_set.handle(p))


if __name__ == "__main__":
    test_lines = read_input("test_input.txt")
    assert part1(test_lines) == 19114

    input_lines = read_input("input.txt")
    print(part1(input_lines))
