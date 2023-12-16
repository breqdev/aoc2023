with open("input.txt") as f:
    grid = [[c for c in line.strip()] for line in f.readlines()]


def tilt_north(grid: list[list[str]]):
    for y in range(1, len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                for y_north in range(y - 1, -1, -1):
                    if grid[y_north][x] != ".":
                        y_north += 1
                        break

                assert y_north == y or (grid[y_north][x] == "." and grid[y][x] == "O")
                grid[y_north][x], grid[y][x] = grid[y][x], grid[y_north][x]


tilt_north(grid)


for line in grid:
    print("".join(line))


def find_load(grid):
    load = 0
    for i, row in enumerate(grid):
        weight = len(grid) - i
        for c in row:
            if c == "O":
                load += weight

    return load


print(find_load(grid))
