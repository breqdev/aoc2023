lines: list[tuple[str, list[int]]] = []

with open("input.txt") as f:
    for line in f.readlines():
        springs_line, groups_line = line.strip().split(" ")
        groups = [int(i) for i in groups_line.split(",")]
        lines.append((springs_line, groups))

print(lines)


def solve_line(
    line: str, groups: list[int], remaining_in_group: int = 0, in_group=False
) -> int:
    if len(line) == 0:
        if len(groups) > 0:
            return 0
        if remaining_in_group > 0:
            return 0

        return 1

    if remaining_in_group > 0:
        if line[0] == ".":
            return 0
        elif line[0] == "#":
            return solve_line(line[1:], groups, remaining_in_group - 1, in_group=True)
        elif line[0] == "?":
            # we need to use it
            return solve_line(line[1:], groups, remaining_in_group - 1, in_group=True)
        else:
            raise ValueError(line[0])
    elif in_group:
        # we are immediately after a group, so this needs to be working
        if line[0] == ".":
            return solve_line(line[1:], groups, in_group=False)
        elif line[0] == "#":
            return 0
        elif line[0] == "?":
            # this needs to be working
            return solve_line(line[1:], groups, in_group=False)
        else:
            raise ValueError(line[0])
    else:
        if line[0] == ".":
            return solve_line(line[1:], groups, in_group=False)
        elif line[0] == "#":
            # we need to use it
            if len(groups) < 1:
                return 0
            return solve_line(line[1:], groups[1:], groups[0] - 1, in_group=True)
        elif line[0] == "?":
            if_working = solve_line(line[1:], groups, in_group=False)
            if_broken = (
                solve_line(line[1:], groups[1:], groups[0] - 1, in_group=True)
                if len(groups) >= 1
                else 0
            )
            return if_working + if_broken
        else:
            raise ValueError(line[0])


print(sum(solve_line(*line) for line in lines))
