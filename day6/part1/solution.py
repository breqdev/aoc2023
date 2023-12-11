from math import sqrt, floor, ceil

with open("input.txt") as f:
    time_strs = f.readline().split()[1:]
    distance_strs = f.readline().split()[1:]

races = [(int(time), int(distance)) for time, distance in zip(time_strs, distance_strs)]

print(races)


def get_intercepts(race_time, record_distance):
    # Quadratic Formula!
    low_intercept = (race_time - sqrt(race_time**2 - 4 * record_distance)) / 2
    high_intercept = (race_time + sqrt(race_time**2 - 4 * record_distance)) / 2
    return (low_intercept, high_intercept)


product = 1

for time, distance in races:
    low, high = get_intercepts(time, distance)
    low, high = floor(low + 1), ceil(high - 1)
    product *= high - low + 1

print(product)
