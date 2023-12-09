import typing

Mapping = typing.NamedTuple(
    "Mapping", [("from_start", int), ("to_start", int), ("length", int)]
)


def parse_input():
    with open("input.txt") as f:
        text = f.read()

    seeds_text, *maps_text = text.split("\n\n")

    seeds_ranges = []
    seeds_values = seeds_text.split(" ")[1:]
    for i in range(0, len(seeds_values), 2):
        seeds_ranges.append(
            (int(seeds_values[i]), int(seeds_values[i]) + int(seeds_values[i + 1]) - 1)
        )

    maps = []
    for map_text in maps_text:
        title_text, *lines_text = map_text.splitlines()
        start_type, _, end_type = title_text.split(" ")[0].split("-")

        mappings = set()

        for line_text in lines_text:
            to_start, from_start, length = line_text.split(" ")
            mappings.add(Mapping(int(from_start), int(to_start), int(length)))

        maps.append(mappings)

    return seeds_ranges, maps


def verify_invariant(union: list[tuple[int, int]]):
    for i in range(1, len(union) - 1):
        assert union[i - 1][1] < union[i][0]
        assert union[i][1] < union[i + 1][0]


def compute_union(intervals: set[tuple[int, int]]) -> list[tuple[int, int]]:
    "Given a set of intervals, return an ordered list of non-overlapping intervals."
    union: list[tuple[int, int]] = []
    for interval in intervals:
        # print(f"Considering interval: {interval}\tUnion: {union}")

        # find the index of the first union-interval with an end greater than this one's start
        for i, candidate in enumerate(union):
            if candidate[1] >= interval[0]:
                # print(f"\tIdentified first potential overlap: {candidate}")
                first_overlap = i
                break
        else:
            # print(f"\tNo first overlap identified")
            first_overlap = None

        # find the index of the last union-interval with a start less than this one's end
        for i, candidate in reversed(list(enumerate(union))):
            if candidate[0] <= interval[1]:
                # print(f"\tIdentified last potential overlap: {candidate}")
                last_overlap = i
                break
        else:
            # print(f"\tNo last overlap identified")
            last_overlap = None

        if last_overlap is None:
            # this is to the left of all existing intervals, and does not overlap
            union.insert(0, interval)
        elif first_overlap is None:
            # this is to the right of all existing intervals, and does not overlap
            union.append(interval)
        elif last_overlap < first_overlap:
            # no intervals overlap this interval
            # insert it after last_overlap
            assert last_overlap + 1 == first_overlap
            union.insert(last_overlap + 1, interval)
        else:
            # we are overlapping intervals and need to merge them
            # this also handles if we overlap a single interval and extend it (i.e., first_overlap == last_overlap)
            new_min = min(union[first_overlap][0], interval[0])
            new_max = max(union[last_overlap][1], interval[1])

            # extend the first interval
            union[first_overlap] = (new_min, new_max)
            union = union[: first_overlap + 1] + union[last_overlap + 1 :]

        # print(f"\tResult: {union}")
        verify_invariant(union)

    return union


def remove_intervals(outer: tuple[int, int], intervals: list[tuple[int, int]]):
    print(f"\t{outer} - {intervals} = ???")
    negated = []

    if outer[1] < intervals[0][0] or outer[0] > intervals[-1][1]:
        print(f"\t\tIntervals do not overlap input range at all -> [{outer}]")
        return [outer]

    if outer[0] < intervals[0][0] <= outer[1]:
        print(
            f"\t\tAdding portion left of first interval: {(outer[0], intervals[0][0] - 1)}"
        )
        negated.append((outer[0], intervals[0][0] - 1))

    for before, after in zip(intervals[:-1], intervals[1:]):
        remaining = (before[1] + 1, after[0] - 1)
        print(f"\t\tConsidering interval gap {remaining}")

        if remaining[0] <= outer[0] <= outer[1] <= remaining[1]:
            print(f"\t\t\tInterval entirely within {outer}")
            negated.append(outer)
        elif outer[0] <= remaining[0] <= outer[1] <= remaining[1]:
            print(f"\t\t\tInterval to left of {outer}")
            negated.append((remaining[0], outer[1]))
        elif remaining[0] <= outer[0] <= remaining[1] <= outer[1]:
            print(f"\t\t\tInterval to right of {outer}")
            negated.append((outer[0], remaining[1]))
        elif outer[0] <= remaining[0] <= remaining[1] <= outer[1]:
            print(f"\t\t\tInterval entirely within {outer}")
            negated.append(remaining)

    if outer[0] <= intervals[-1][1] < outer[1]:
        print(
            f"\t\tAdding portion right of last interval: {(intervals[-1][1] + 1, outer[1])}"
        )
        negated.append((intervals[-1][1] + 1, outer[1]))

    verify_invariant(negated)
    print(f"\t\t\t-> {negated}")
    return negated


def map_range(map: set[Mapping], range: tuple[int, int]) -> set[tuple[int, int]]:
    # order the mappings in the "from" range
    mappings = sorted(map, key=lambda mapping: mapping.from_start)
    # find the intervals in the range-to-map not covered by the mappings
    null_mapping = remove_intervals(
        range,
        compute_union(
            set(
                (mapping.from_start, mapping.from_start + mapping.length)
                for mapping in mappings
            )
        ),
    )

    mapped_ranges = set(null_mapping)

    for mapping in mappings:
        if (
            mapping.from_start
            <= range[0]
            <= range[1]
            <= mapping.from_start + mapping.length
        ):
            # Map only the range contained within
            mapped_ranges.add(
                (
                    (range[0] - mapping.from_start) + mapping.to_start,
                    (range[1] - mapping.from_start) + mapping.to_start,
                )
            )
        elif (
            range[0]
            <= mapping.from_start
            <= range[1]
            <= mapping.from_start + mapping.length
        ):
            mapped_ranges.add(
                (mapping.to_start, (range[1] - mapping.from_start) + mapping.to_start)
            )
        elif (
            mapping.from_start
            <= range[0]
            <= mapping.from_start + mapping.length
            <= range[1]
        ):
            mapped_ranges.add(
                (
                    (range[0] - mapping.from_start) + mapping.to_start,
                    mapping.to_start + mapping.length,
                )
            )
        elif (
            range[0]
            <= mapping.from_start
            <= mapping.from_start + mapping.length
            <= range[1]
        ):
            mapped_ranges.add(
                (
                    mapping.to_start,
                    mapping.to_start + mapping.length,
                )
            )

    return mapped_ranges


def map_ranges(
    map: set[Mapping], ranges: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    result_ranges = set()
    for range in ranges:
        result_ranges.update(map_range(map, range))

    return compute_union(result_ranges)


def full_map_ranges(maps: list[set[Mapping]], ranges: set[tuple[int, int]]):
    ranges_list = compute_union(ranges)

    for map in maps:
        print(ranges_list)
        ranges_list = map_ranges(map, set(ranges_list))

    return ranges_list


def main():
    seeds_ranges, maps = parse_input()
    results = full_map_ranges(maps, seeds_ranges)
    print(results[0][0])


main()
