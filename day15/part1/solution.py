def HASH(input: str):
    value = 0
    for c in input:
        ascii = ord(c)
        value += ascii
        value *= 17
        value %= 256
    return value


with open("input.txt") as f:
    parts = f.read().strip().split(",")

print(sum(HASH(part) for part in parts))
