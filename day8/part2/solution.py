import itertools

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

current_nodes = [node for node in nodes if node.endswith("A")]

for i in itertools.count():
    instruction = instructions[i % len(instructions)]
    if instruction == "L":
        current_nodes = [nodes[node][0] for node in current_nodes]
    elif instruction == "R":
        current_nodes = [nodes[node][1] for node in current_nodes]
    # print(node)
    if all(node.endswith("Z") for node in current_nodes):
        break

print(i + 1)
