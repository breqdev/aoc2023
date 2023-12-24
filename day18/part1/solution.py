from shapely.geometry import Point, Polygon

current = (0, 0)
polygon_points = [current]

with open("input.txt") as f:
    for line in f.readlines():
        direction, distance_str, color = line.split(" ")

        distance = int(distance_str)
        x, y = current

        if direction == "U":
            current = (x, y - distance)
        elif direction == "D":
            current = (x, y + distance)
        elif direction == "L":
            current = (x - distance, y)
        elif direction == "R":
            current = (x + distance, y)
        else:
            raise ValueError(direction)

        polygon_points.append(current)

polygon = Polygon(polygon_points[:-1])

print(polygon.length)

within = 0

for x in range(
    min(x for x, y in polygon_points), max(x for x, y in polygon_points) + 1
):
    for y in range(
        min(y for x, y in polygon_points), max(y for x, y in polygon_points) + 1
    ):
        if polygon.contains_properly(Point(x, y)):
            within += 1

print(within)
print(within + polygon.length)
