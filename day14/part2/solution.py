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


def tilt_west(grid: list[list[str]]):
    for y in range(len(grid)):
        for x in range(1, len(grid[0])):
            if grid[y][x] == "O":
                for x_west in range(x - 1, -1, -1):
                    if grid[y][x_west] != ".":
                        x_west += 1
                        break

                assert x_west == x or (grid[y][x_west] == "." and grid[y][x] == "O")
                grid[y][x_west], grid[y][x] = grid[y][x], grid[y][x_west]


def tilt_south(grid: list[list[str]]):
    for y in range(len(grid) - 2, -1, -1):
        for x in range(len(grid[0])):
            if grid[y][x] == "O":
                for y_south in range(y + 1, len(grid)):
                    if grid[y_south][x] != ".":
                        y_south -= 1
                        break

                assert y_south == y or (grid[y_south][x] == "." and grid[y][x] == "O")
                grid[y_south][x], grid[y][x] = grid[y][x], grid[y_south][x]


def tilt_east(grid: list[list[str]]):
    for y in range(len(grid)):
        for x in range(len(grid[0]) - 2, -1, -1):
            if grid[y][x] == "O":
                for x_east in range(x + 1, len(grid[0])):
                    if grid[y][x_east] != ".":
                        x_east -= 1
                        break

                assert x_east == x or (grid[y][x_east] == "." and grid[y][x] == "O")
                grid[y][x_east], grid[y][x] = grid[y][x], grid[y][x_east]


def find_load(grid):
    load = 0
    for i, row in enumerate(grid):
        weight = len(grid) - i
        for c in row:
            if c == "O":
                load += weight

    return load


def billion_rotations(grid: list[list[str]]):
    scratchpad = [row.copy() for row in grid]
    states = [[row.copy() for row in scratchpad]]

    while scratchpad not in states[:-1]:
        tilt_north(scratchpad)
        tilt_west(scratchpad)
        tilt_south(scratchpad)
        tilt_east(scratchpad)
        states.append([row.copy() for row in scratchpad])

    start_val = len(states)

    target = states[-1]
    for i, state in enumerate(states):
        if state == target:
            break

    first_occurrence = i
    last_occurrence = len(states) - 1
    period = last_occurrence - first_occurrence

    target_count = start_val + (1000000000 - start_val) % period

    for _ in range(target_count):
        tilt_north(grid)
        tilt_west(grid)
        tilt_south(grid)
        tilt_east(grid)


billion_rotations(grid)

for line in grid:
    print("".join(line))


print(find_load(grid))
