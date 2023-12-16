from typing import Literal

Direction = Literal["n"] | Literal["e"] | Literal["s"] | Literal["w"]

opposites: dict[Direction, Direction] = {"n": "s", "e": "w", "s": "n", "w": "e"}


traverse: dict[Direction, tuple[int, int]] = {
    "n": (0, -1),
    "e": (1, 0),
    "s": (0, 1),
    "w": (-1, 0),
}


class Tile:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type
        self.illuminated_from: dict[Direction, bool] = {
            "n": False,
            "e": False,
            "s": False,
            "w": False,
        }

    def __repr__(self):
        return self.type

    def light_in(self, dir: Direction) -> bool:
        if self.illuminated_from[dir]:
            return False
        else:
            self.illuminated_from[dir] = True
            return True

    @property
    def light_out(self) -> set[Direction]:
        illuminates = set()
        if self.type == ".":
            for dir, lit in self.illuminated_from.items():
                if lit:
                    illuminates.add(opposites[dir])
        elif self.type == "/":
            if self.illuminated_from["n"]:
                illuminates.add("w")
            if self.illuminated_from["e"]:
                illuminates.add("s")
            if self.illuminated_from["s"]:
                illuminates.add("e")
            if self.illuminated_from["w"]:
                illuminates.add("n")
        elif self.type == "\\":
            if self.illuminated_from["n"]:
                illuminates.add("e")
            if self.illuminated_from["e"]:
                illuminates.add("n")
            if self.illuminated_from["s"]:
                illuminates.add("w")
            if self.illuminated_from["w"]:
                illuminates.add("s")
        elif self.type == "|":
            if self.illuminated_from["n"]:
                illuminates.add("s")
            if self.illuminated_from["s"]:
                illuminates.add("n")
            if self.illuminated_from["e"] or self.illuminated_from["w"]:
                illuminates.add("n")
                illuminates.add("s")
        elif self.type == "-":
            if self.illuminated_from["e"]:
                illuminates.add("w")
            if self.illuminated_from["w"]:
                illuminates.add("e")
            if self.illuminated_from["n"] or self.illuminated_from["s"]:
                illuminates.add("e")
                illuminates.add("w")
        return illuminates


grid: list[list[Tile]] = []

with open("input.txt") as f:
    for y, line in enumerate(f.readlines()):
        grid.append([Tile(x, y, c) for x, c in enumerate(line.strip())])

grid[0][0].light_in("w")
unsettled: set[Tile] = {grid[0][0]}

while unsettled:
    tile = unsettled.pop()
    for neighbor_dir in tile.light_out:
        x_diff, y_diff = traverse[neighbor_dir]
        if 0 <= tile.y + y_diff < len(grid) and 0 <= tile.x + x_diff < len(grid[0]):
            neighbor = grid[tile.y + y_diff][tile.x + x_diff]
            needs_update = neighbor.light_in(opposites[neighbor_dir])
            if needs_update:
                unsettled.add(neighbor)

energized = 0
for row in grid:
    for tile in row:
        if any(tile.illuminated_from.values()):
            energized += 1

print(energized)
