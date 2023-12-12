from enum import Enum


class Direction(Enum):
    NORTH = (0, -1)
    EAST = (1, 0)
    SOUTH = (0, 1)
    WEST = (-1, 0)


pipe_chars = {
    "|": set((Direction.NORTH, Direction.SOUTH)),
    "-": set((Direction.EAST, Direction.WEST)),
    "L": set((Direction.NORTH, Direction.EAST)),
    "J": set((Direction.NORTH, Direction.WEST)),
    "7": set((Direction.SOUTH, Direction.WEST)),
    "F": set((Direction.SOUTH, Direction.EAST)),
}

opposites = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}


def traverse(pipe_char: str, from_dir: Direction) -> Direction | None:
    directions = pipe_chars[pipe_char]
    if opposites[from_dir] not in directions:
        return None

    other = next(i for i in directions if i != opposites[from_dir])
    return other


with open("input.txt") as f:
    grid = [[i for i in line.strip()] for line in f.readlines()]

for y, line in enumerate(grid):
    if "S" in line:
        start_pos = (line.index("S"), y)


# Try to traverse in each direction until something works
def travel(posn: tuple[int, int], dir: Direction):
    return (posn[0] + dir.value[0], posn[1] + dir.value[1])


def get_char(posn: tuple[int, int]):
    global grid
    return grid[posn[1]][posn[0]]


for start_pipe_dir in [
    Direction.NORTH,
    Direction.SOUTH,
    Direction.EAST,
    Direction.WEST,
]:
    start_pipe_posn = travel(start_pos, start_pipe_dir)
    start_pipe_char = get_char(start_pipe_posn)
    if (
        start_pipe_char in pipe_chars
        and opposites[start_pipe_dir] in pipe_chars[start_pipe_char]
    ):
        break

posn = start_pipe_posn
from_dir = start_pipe_dir

steps = 0
while True:
    print(posn, get_char(posn), from_dir)
    next_dir = traverse(get_char(posn), from_dir)
    assert next_dir
    posn = travel(posn, next_dir)
    from_dir = next_dir
    steps += 1
    if get_char(posn) == "S":
        break

print(steps // 2 + 1)
