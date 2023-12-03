import dataclasses

grid: list[list[str]] = []

with open("input.txt") as f:
    for line in f.readlines():
        grid.append([c for c in line])

@dataclasses.dataclass
class Number:
    value: int = -1
    row: int = -1
    start_col: int = -1
    end_col: int = -1

@dataclasses.dataclass
class Gear:
    col: int = -1
    row: int = -1

semantic_grid = []
gears: list[Gear] = []

for y, row in enumerate(grid):
    new_row: list[Number | Gear | None] = []
    current_number: Number | None = None

    for x, c in enumerate(row):
        if c.isdigit():
            if current_number:
                current_number.value = current_number.value * 10 + int(c)
                current_number.end_col = x
            else:
                current_number = Number(int(c), y, x, x)
            new_row.append(current_number)
        elif c == ".":
            current_number = None
            new_row.append(None)
        elif c == "\n":
            continue
        elif c == "*":
            current_number = None
            gear = Gear(x, y)
            new_row.append(gear)
            gears.append(gear)
        else:
            current_number = None
            new_row.append(None)

    semantic_grid.append(new_row)

def check_number(x, y) -> Number | None:
    if x < 0 or y < 0 or y >= len(semantic_grid) or x >= len(semantic_grid[y]):
        return None
    if isinstance(semantic_grid[y][x], Number):
        return semantic_grid[y][x]
    else:
        return None

gear_sum = 0
for gear in gears:
    candidates = [
        check_number(gear.col - 1, gear.row - 1),
        check_number(gear.col - 1, gear.row),
        check_number(gear.col - 1, gear.row + 1),
        check_number(gear.col, gear.row - 1),
        check_number(gear.col, gear.row),
        check_number(gear.col, gear.row + 1),
        check_number(gear.col + 1, gear.row - 1),
        check_number(gear.col + 1, gear.row),
        check_number(gear.col + 1, gear.row + 1),
    ]

    # enforce uniqueness
    # we need the value, but we need to enforce uniqueness over the object
    numbers: set[tuple[int, int]] = set((id(n), n.value) for n in candidates if n)

    if len(numbers) == 2:
        numbers_list = list(numbers)
        gear_sum += numbers_list[0][1] * numbers_list[1][1]

print(gear_sum)
