import re

number_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def calibration_value(line: str):
    first_match = re.search(r"([0-9]|zero|one|two|three|four|five|six|seven|eight|nine)", line)
    last_match = re.search(r".*([0-9]|zero|one|two|three|four|five|six|seven|eight|nine).*$", line)
    assert first_match and last_match, line
    if first_match.group(1).isdigit():
        first = int(first_match.group(1))
    else:
        first = number_names.index(first_match.group(1))
    if last_match.group(1).isdigit():
        last = int(last_match.group(1))
    else:
        last = number_names.index(last_match.group(1))
    return int(str(first) + str(last))

with open("input.txt") as f:
    print(sum(calibration_value(line) for line in f.readlines()))
