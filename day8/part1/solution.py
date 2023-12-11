import itertools

with open("input.txt") as f:
    instructions, _, *node_strs = f.readlines()

nodes = {}
for line in node_strs:
    name, dests = line.split("=")
    left, right = dests.split(",")
    name = name.strip()
    left, right = left.removeprefix(" ("), right.strip().removesuffix(")")
    nodes[name] = (left, right)

print(nodes)

instructions = instructions.strip()

node = "AAA"
for i in itertools.count():
    instruction = instructions[i % len(instructions)]
    if instruction == "L":
        node = nodes[node][0]
    elif instruction == "R":
        node = nodes[node][1]
    # print(node)
    if node == "ZZZ":
        break

print(i + 1)
