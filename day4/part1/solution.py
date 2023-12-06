with open("input.txt") as f:
    card_lines = f.readlines()

sum_score = 0
for line in card_lines:
    label, line = line.strip().split(":")
    winning_part, have_part = line.split("|")
    winning = set(int(n) for n in winning_part.strip().split(" ") if n)
    have = [int(n) for n in have_part.strip().split(" ") if n]

    score = 0
    for n in have:
        if n in winning:
            if score == 0:
                score = 1
            else:
                score *= 2

    # print(label, score)
    sum_score += score

print(sum_score)
