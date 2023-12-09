import typing

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


def compute_intersection(intervals: set[tuple[int, int]]) -> list[tuple[int, int]]:
    "Given a set of intervals, return an ordered list of non-overlapping intervals."
    intersection: list[tuple[int, int]] = []
    for interval in intervals:
        # find the index of the first intersection-interval with an end greater than this one's start
        for i, candidate in enumerate(intersection):
            if candidate[1] >= interval[0]:
                first_overlap = i
                break
        else:
            first_overlap = None

        # find the index of the last intersection-interval with a start less than this one's end
        for i, candidate in reversed(list(enumerate(intersection))):
            if candidate[0] <= interval[1]:
                last_overlap = i
                break
        else:
            last_overlap = None

        if first_overlap is None:
            # this is to the left of all existing intervals, and does not overlap
            intersection.insert(0, interval)
        elif last_overlap is None:
            # this is to the right of all existing intervals, and does not overlap
            intersection.append(interval)
        elif last_overlap < first_overlap:
            # no intervals overlap this interval
            # insert it after last_overlap
            assert last_overlap + 1 == first_overlap
            intersection.insert(last_overlap + 1, interval)
        else:
            # we are overlapping intervals and need to merge them
            # this also handles if we overlap a single interval and extend it (i.e., first_overlap == last_overlap)
            new_min = min(intersection[first_overlap][0], interval[0])
            new_max = max(intersection[last_overlap][1], interval[1])

            # extend the first interval
            intersection[first_overlap] = (new_min, new_max)
            intersection = (
                intersection[: first_overlap + 1] + intersection[last_overlap:]
            )

    return intersection


def map_range(map: set[Mapping], start: int, end: int):
    ranges = set()
    for mapping in map:
        mapped_start = mapping.to_start + (start - mapping.from_start)
        mapped_end = mapping.to_start + (end - mapping.from_start)
        if mapping.from_start <= start <= end <= mapping.from_start + mapping.length:
            # range entirely contained within mapping
            ranges.add((mapped_start, mapped_end))
        elif mapping.from_start <= start <= mapping.from_start + mapping.length <= end:
            # range extends to the right of the mapping
            ranges.add((mapped_start, mapping.to_start + mapping.length))
        elif start <= mapping.from_start <= end <= mapping.from_start + mapping.length:
            # range extends to the left of the mapping
            ranges.add((mapping.to_start, mapped_end))
    # TODO: what about the mapping not in range?

    return ranges


def perform_mappings(maps: list[set[Mapping]], start: int, end: int):
    ranges = [(start, end)]
    for map in maps:
        new_ranges = []
        for range in ranges:
            new_ranges += map_range(map, range[0], range[1])
        ranges = new_ranges
    return ranges


print(perform_mappings(maps, 79, 79 + 14))
