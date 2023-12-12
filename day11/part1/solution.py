import itertools

galaxies = []

with open("input.txt") as f:
    for y, line in enumerate(f.readlines()):
        for x, char in enumerate(line.strip()):
            if char == "#":
                galaxies.append((x, y))

num_cols, num_rows = x + 1, y + 1
empty_cols, empty_rows = set(range(num_cols)), set(range(num_rows))

for x, y in galaxies:
    empty_cols.discard(x)
    empty_rows.discard(y)

print(empty_cols, empty_rows)

# Stretch horizontally
map_x: list[int] = []
for x in range(num_cols):
    map_x.append(x + len(set(c for c in empty_cols if c < x)))

map_y: list[int] = []
for y in range(num_rows):
    map_y.append(y + len(set(r for r in empty_rows if r < y)))

galaxies = [(map_x[x], map_y[y]) for (x, y) in galaxies]

print(galaxies)

sum_paths = 0
for left, right in itertools.combinations(galaxies, 2):
    sum_paths += abs(left[0] - right[0]) + abs(left[1] - right[1])

print(sum_paths)
