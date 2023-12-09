import typing
import itertools

Mapping = typing.NamedTuple(
    "Mapping", [("from_start", int), ("to_start", int), ("length", int)]
)


def parse_input():
    with open("sample.txt") as f:
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


def perform_mapping_reversed(map: set[Mapping], value: int):
    for mapping in map:
        if value >= mapping.to_start and value < mapping.to_start + mapping.length:
            offset = value - mapping.to_start
            return mapping.from_start + offset

    return value


def perform_mappings_reversed(maps: list[set[Mapping]], value: int):
    for map in reversed(maps):
        value = perform_mapping_reversed(map, value)
    return value


for location in itertools.count():
    maybe_seed = perform_mappings_reversed(maps, location)
    if maybe_seed in seeds:
        print(location)
        break
