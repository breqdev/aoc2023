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
class Symbol:
    pass

semantic_grid = []
numbers: list[Number] = []

for y, row in enumerate(grid):
    new_row: list[Number | Symbol | None] = []
    current_number: Number | None = None

    for x, c in enumerate(row):
        if c.isdigit():
            if current_number:
                current_number.value = current_number.value * 10 + int(c)
                current_number.end_col = x
            else:
                current_number = Number(int(c), y, x, x)
                numbers.append(current_number)
            new_row.append(current_number)
        elif c == ".":
            current_number = None
            new_row.append(None)
        elif c == "\n":
            continue
        else:
            current_number = None
            new_row.append(Symbol())

    semantic_grid.append(new_row)

def check_symbol(x, y):
    if x < 0 or y < 0 or y >= len(semantic_grid) or x >= len(semantic_grid[y]):
        return False
    return isinstance(semantic_grid[y][x], Symbol)

valid_pns = []
for number in numbers:
    # check left side
    if check_symbol(number.start_col - 1, number.row - 1) or check_symbol(number.start_col - 1, number.row) or check_symbol(number.start_col - 1, number.row + 1):
        valid_pns.append(number)
        continue

    # check right side
    if check_symbol(number.end_col + 1, number.row - 1) or check_symbol(number.end_col + 1, number.row) or check_symbol(number.end_col + 1, number.row + 1):
        valid_pns.append(number)
        continue

    # check above or below
    for col in range(number.start_col, number.end_col + 1):
        assert isinstance(semantic_grid[number.row][col], Number)
        if check_symbol(col, number.row - 1) or check_symbol(col, number.row + 1):
            valid_pns.append(number)
            continue

print(sum(pn.value for pn in valid_pns))
