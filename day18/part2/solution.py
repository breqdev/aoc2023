from shapely.geometry import Polygon

current = (0, 0)
polygon_points = [current]

with open("input.txt") as f:
    for line in f.readlines():
        _, _, color = line.split(" ")
        color = color.strip("(#)\n")
        distance = int(color[:-1], base=16)
        direction = color[-1]

        x, y = current

        if direction == "3":
            current = (x, y - distance)
        elif direction == "1":
            current = (x, y + distance)
        elif direction == "2":
            current = (x - distance, y)
        elif direction == "0":
            current = (x + distance, y)
        else:
            raise ValueError(direction)

        polygon_points.append(current)

polygon = Polygon(polygon_points[:-1])

print(polygon.length)

# Pick's theorem in reverse
interior = polygon.area - (polygon.length / 2) + 1
print(interior)
print(interior + polygon.length)
