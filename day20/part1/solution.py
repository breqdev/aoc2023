from dataclasses import dataclass
from queue import Queue


@dataclass(frozen=True)
class Pulse:
    from_node: str
    to_node: str
    level: bool

    def __repr__(self):
        return f"{self.from_node} -{'high' if self.level else 'low'}-> {self.to_node}"


class Node:
    name: str
    outputs: list[str]
    inputs: list[str] = []

    def __init__(self, name: str, destinations: list[str]):
        self.name = name
        self.outputs = destinations

    def add_input(self, input_node: str):
        self.inputs.append(input_node)

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        return []

    def __repr__(self):
        return f"{self.inputs} -> {self.name} -> {self.outputs}"


class FlipFlopNode(Node):
    state: bool = False

    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        output = []
        if pulse.level:
            pass
        else:
            if self.state:
                # print(f"{self.name} flipping OFF")
                self.state = False
                for dest_name in self.outputs:
                    output.append(
                        Pulse(from_node=self.name, to_node=dest_name, level=False)
                    )
            else:
                # print(f"{self.name} flipping ON")
                self.state = True
                for dest_name in self.outputs:
                    output.append(
                        Pulse(from_node=self.name, to_node=dest_name, level=True)
                    )
        return output


class ConjunctionNode(Node):
    last_pulses: dict[str, bool]

    def __init__(self, name: str, destinations: list[str]):
        self.last_pulses = {}
        super().__init__(name, destinations)

    def add_input(self, input: str):
        self.last_pulses[input] = False
        return super().add_input(input)

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        assert pulse.from_node in self.last_pulses
        self.last_pulses[pulse.from_node] = pulse.level
        output = []
        # print(f"{self.name} remembers {self.last_pulses}")
        if all(self.last_pulses.values()):
            for dest_name in self.outputs:
                output.append(
                    Pulse(from_node=self.name, to_node=dest_name, level=False)
                )
        else:
            for dest_name in self.outputs:
                output.append(Pulse(from_node=self.name, to_node=dest_name, level=True))
        return output


class BroadcasterNode(Node):
    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)

    def receive_pulse(self, pulse: Pulse) -> list[Pulse]:
        output = []
        for dest_name in self.outputs:
            output.append(
                Pulse(from_node=self.name, to_node=dest_name, level=pulse.level)
            )
        return output


nodes: dict[str, Node] = {}

with open("input.txt") as f:
    for line in f.readlines():
        node_part, dest_part = line.strip().split(" -> ")
        destinations = dest_part.split(", ")

        if node_part == "broadcaster":
            nodes["broadcaster"] = BroadcasterNode("broadcaster", destinations)
        else:
            type = node_part[0]
            name = node_part[1:]
            if type == "&":
                nodes[name] = ConjunctionNode(name, destinations)
            elif type == "%":
                nodes[name] = FlipFlopNode(name, destinations)
            else:
                raise ValueError(type)

# Reverse the edges
for from_node in nodes.values():
    for to_node in from_node.outputs:
        if to_node in nodes:
            # print(f"Relation: {from_node.name} -> {to_node}")
            nodes[to_node].add_input(from_node.name)

# print(nodes)


def evaluate(nodes: dict[str, Node]):
    pulses: Queue[Pulse] = Queue()
    pulses.put(Pulse("button", "broadcaster", False))

    high_count, low_count = 0, 0

    while not pulses.empty():
        pulse = pulses.get()
        # print(pulse)
        if pulse.level:
            high_count += 1
        else:
            low_count += 1

        if pulse.to_node in nodes:
            new_pulses = nodes[pulse.to_node].receive_pulse(pulse)
            for new_pulse in new_pulses:
                pulses.put(new_pulse)

    return high_count, low_count


total_high, total_low = 0, 0
for i in range(1000):
    high, low = evaluate(nodes)
    total_high += high
    total_low += low

print(total_high * total_low)
