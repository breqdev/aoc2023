import typing

Mapping = typing.NamedTuple(
    "Mapping", [("from_start", int), ("to_start", int), ("length", int)]
)


def parse_input():
    with open("input.txt") as f:
        text = f.read()

    seeds_text, *maps_text = text.split("\n\n")

    seeds = [int(i.strip()) for i in seeds_text.removeprefix("seeds: ").split(" ")]

    maps = []
    for map_text in maps_text:
        title_text, *lines_text = map_text.splitlines()
        start_type, _, end_type = title_text.split(" ")[0].split("-")

        mappings = set()

        for line_text in lines_text:
            to_start, from_start, length = line_text.split(" ")
            mappings.add(Mapping(int(from_start), int(to_start), int(length)))

        maps.append(mappings)

    return seeds, maps


seeds, maps = parse_input()


def perform_mapping(map: set[Mapping], value: int):
    for mapping in map:
        if value >= mapping.from_start and value < mapping.from_start + mapping.length:
            offset = value - mapping.from_start
            return mapping.to_start + offset

    return value


def perform_mappings(maps: list[set[Mapping]], value: int):
    for map in maps:
        value = perform_mapping(map, value)
    return value


locations = set()
for seed in seeds:
    locations.add(perform_mappings(maps, seed))

print(min(locations))
