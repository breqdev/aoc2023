def calibration_value(line: str):
    numbers = [c for c in line if c.isdigit()]
    return int(numbers[0] + numbers[-1])

with open("input.txt") as f:
    print(sum(calibration_value(line) for line in f.readlines()))
