import itertools
import math

with open("input.txt") as f:
    instructions, _, *node_strs = f.readlines()

nodes: dict[str, tuple[str, str]] = {}
for line in node_strs:
    name, dests = line.split("=")
    left, right = dests.split(",")
    name = name.strip()
    left, right = left.removeprefix(" ("), right.strip().removesuffix(")")
    nodes[name] = (left, right)

print(nodes)

instructions = instructions.strip()

start_nodes = [node for node in nodes if node.endswith("A")]


def get_period(node: str) -> int:
    for i in itertools.count():
        instruction = instructions[i % len(instructions)]
        if instruction == "L":
            node = nodes[node][0]
        elif instruction == "R":
            node = nodes[node][1]
        if node.endswith("Z"):
            break

    return i + 1


print(math.lcm(*(get_period(node) for node in start_nodes)))
