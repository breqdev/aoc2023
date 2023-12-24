with open("sample.txt") as f:
    grid = [[int(c) for c in line.strip()] for line in f.readlines()]

unvisited: set[tuple[int, int]] = set(
    (x, y) for y, row in enumerate(grid) for x, _ in enumerate(row)
)
distances: dict[tuple[int, int], int] = {(0, 0): 0}
current = (0, 0)
destination = (len(grid[0]) - 1, len(grid) - 1)


def weight(node: tuple[int, int]):
    x, y = node
    return grid[y][x]


def neighbors(node: tuple[int, int]):
    x, y = node
    result: set[tuple[int, int]] = set()

    if x > 0:
        result.add((x - 1, y))
    if x < len(grid[0]) - 1:
        result.add((x + 1, y))
    if y > 0:
        result.add((x, y - 1))
    if y < len(grid) - 1:
        result.add((x, y + 1))
    return result


while destination in unvisited:
    for neighbor in neighbors(current):
        if neighbor in unvisited:
            distance = distances[current] + weight(current)
            if neighbor in distances:
                distances[neighbor] = min(distances[neighbor], distance)
            else:
                distances[neighbor] = distance
    unvisited.remove(current)
    current = min(unvisited, key=lambda n: distances.get(n, float("inf")))

print(distances[destination])
