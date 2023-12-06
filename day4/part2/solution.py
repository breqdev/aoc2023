with open("input.txt") as f:
    card_lines = f.readlines()

copies = [1 for _ in range(len(card_lines))]

for i, line in enumerate(card_lines):
    label, line = line.strip().split(":")
    winning_part, have_part = line.split("|")
    winning = set(int(n) for n in winning_part.strip().split(" ") if n)
    have = [int(n) for n in have_part.strip().split(" ") if n]

    num_winning = 0
    for n in have:
        if n in winning:
            num_winning += 1

    for j in range(i + 1, i + num_winning + 1):
        copies[j] += copies[i]

print(sum(copies))
