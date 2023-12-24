from dataclasses import dataclass


@dataclass
class Rule:
    target: str  # x, m, a, s
    operator: str  # < or >
    threshold: int
    destination: str


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    default: str


@dataclass
class Range:
    min_val: int
    max_val: int

    def copy(self):
        return Range(self.min_val, self.max_val)

    def size(self):
        return self.max_val - self.min_val + 1


@dataclass
class Area:
    x: Range
    m: Range
    a: Range
    s: Range

    def copy(self):
        return Area(self.x.copy(), self.m.copy(), self.a.copy(), self.s.copy())

    def size(self):
        return self.x.size() * self.m.size() * self.a.size() * self.s.size()

    def __getitem__(self, key: str):
        if key == "x":
            return self.x
        if key == "m":
            return self.m
        if key == "a":
            return self.a
        if key == "s":
            return self.s
        raise ValueError(key)


with open("sample.txt") as f:
    workflow_text, parts_text = f.read().split("\n\n")

workflows: dict[str, Workflow] = {}
for line in workflow_text.split("\n"):
    name, workflow_part = line.removesuffix("}").split("{")
    rules = []
    rule_parts = workflow_part.split(",")
    for rule_part in rule_parts[:-1]:
        condition_part, destination = rule_part.split(":")
        target = condition_part[0]
        operator = condition_part[1]
        threshold = int(condition_part[2:])
        rules.append(Rule(target, operator, threshold, destination))
    workflows[name] = Workflow(name, rules, default=rule_parts[-1])


def get_accepted_ranges(
    workflow: Workflow, workflows: dict[str, Workflow], covered: Area
) -> list[Area]:
    accepted: list[Area] = []
    remaining = covered.copy()

    for rule in workflow.rules:
        covered = remaining.copy()

        if rule.operator == "<":
            covered[rule.target].max_val = rule.threshold - 1
            remaining[rule.target].min_val = rule.threshold
        elif rule.operator == ">":
            covered[rule.target].min_val = rule.threshold + 1
            remaining[rule.target].max_val = rule.threshold
        else:
            raise ValueError(rule.operator)

        if rule.destination == "A":
            accepted.append(covered)
        elif rule.destination != "R":
            accepted.extend(
                get_accepted_ranges(workflows[rule.destination], workflows, covered)
            )

    if workflow.default == "A":
        accepted.append(remaining)
    elif workflow.default != "R":
        accepted.extend(
            get_accepted_ranges(workflows[workflow.default], workflows, remaining)
        )
    return accepted


areas = get_accepted_ranges(
    workflows["in"],
    workflows,
    Area(Range(1, 4000), Range(1, 4000), Range(1, 4000), Range(1, 4000)),
)

total = 0
for area in areas:
    total += area.size()

print(total)
