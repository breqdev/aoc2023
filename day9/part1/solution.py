with open("input.txt") as f:
    lines = f.readlines()

sequences = [[int(i) for i in line.split()] for line in lines]
print(sequences)


def predict_next(sequence):
    if all(i == 0 for i in sequence):
        return 0

    differences = [(right - left) for left, right in zip(sequence[:-1], sequence[1:])]
    next_difference = predict_next(differences)
    return sequence[-1] + next_difference


result = 0
for sequence in sequences:
    result += predict_next(sequence)

print(result)
