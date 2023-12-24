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
class Part:
    x: int
    m: int
    a: int
    s: int

    @property
    def total(self):
        return self.x + self.m + self.a + self.s


with open("input.txt") as f:
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

parts: list[Part] = []
for line in parts_text.split("\n"):
    if not line:
        break

    x_part, m_part, a_part, s_part = line.removeprefix("{").removesuffix("}").split(",")

    x = int(x_part.removeprefix("x="))
    m = int(m_part.removeprefix("m="))
    a = int(a_part.removeprefix("a="))
    s = int(s_part.removeprefix("s="))

    parts.append(Part(x, m, a, s))


def evaluate_workflow(part: Part, workflow: Workflow) -> str:
    for rule in workflow.rules:
        value: int = getattr(part, rule.target)
        if rule.operator == "<":
            if value < rule.threshold:
                return rule.destination
        elif rule.operator == ">":
            if value > rule.threshold:
                return rule.destination
        else:
            raise ValueError(rule.operator)
    return workflow.default


def evaluate_part(part: Part, workflows: dict[str, Workflow]) -> bool:
    workflow_name = "in"

    while workflow_name not in ["A", "R"]:
        workflow = workflows[workflow_name]
        workflow_name = evaluate_workflow(part, workflow)

    return workflow_name == "A"


total = 0
for part in parts:
    if evaluate_part(part, workflows):
        total += part.total

print(total)
