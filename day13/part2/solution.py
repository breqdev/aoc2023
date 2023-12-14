with open("input.txt") as f:
    groups_text = f.read().split("\n\n")

patterns = []

for group in groups_text:
    pattern = []
    for line in group.split("\n"):
        if line:
            pattern.append([c for c in line])
    patterns.append(pattern)


def check_reflection_x(pattern: list[list[str]], axis: int):
    for distance in range(min(axis, len(pattern[0]) - axis)):
        for y in range(len(pattern)):
            row = pattern[y]
            if row[axis - distance - 1] != row[axis + distance]:
                return False
    return True


def check_reflection_y(pattern: list[list[str]], axis: int):
    for distance in range(min(axis, len(pattern) - axis)):
        row_upper = pattern[axis - distance - 1]
        row_lower = pattern[axis + distance]
        for x in range(len(pattern[0])):
            if row_upper[x] != row_lower[x]:
                return False
    return True


def find_reflection(pattern: list[list[str]], skip=None):
    for x_axis in range(1, len(pattern[0])):
        if check_reflection_x(pattern, x_axis):
            if skip != ("x", x_axis):
                return ("x", x_axis)
    for y_axis in range(1, len(pattern)):
        if check_reflection_y(pattern, y_axis):
            if skip != ("y", y_axis):
                return ("y", y_axis)

    return None


def find_smudge(pattern: list[list[str]]):
    original_reflection = find_reflection(pattern)

    for smudge_x in range(len(pattern[0])):
        for smudge_y in range(len(pattern)):
            if pattern[smudge_y][smudge_x] == "#":
                pattern[smudge_y][smudge_x] = "."
            elif pattern[smudge_y][smudge_x] == ".":
                pattern[smudge_y][smudge_x] = "#"

            result = find_reflection(pattern, skip=original_reflection)
            if result:
                return result

            if pattern[smudge_y][smudge_x] == "#":
                pattern[smudge_y][smudge_x] = "."
            elif pattern[smudge_y][smudge_x] == ".":
                pattern[smudge_y][smudge_x] = "#"


reflections = [find_smudge(pattern) for pattern in patterns]


summary = 0
for dir, axis in reflections:
    if dir == "x":
        summary += axis
    else:
        summary += axis * 100

print(summary)
