from functools import cmp_to_key

with open("input.txt") as f:
    hand_strs = f.readlines()

hands = []
for line in hand_strs:
    hand, bid = line.split(" ")
    hands.append((hand, int(bid)))


def rank(hand_str: str):
    assert len(hand_str) == 5
    hand = sorted(hand_str)
    # check five of a kind
    if hand[0] == hand[4]:
        return 0
    # check four of a kind
    if hand[0] == hand[3] or hand[1] == hand[4]:
        return 1
    # check full house
    if (hand[0] == hand[1] and hand[2] == hand[4]) or (
        hand[0] == hand[2] and hand[3] == hand[4]
    ):
        return 2
    # check three kind
    if hand.count(hand[2]) == 3:
        return 3
    # check two pair
    if (hand.count(hand[0]) == 2) + (hand.count(hand[2]) == 2) + (
        hand.count(hand[4]) == 2
    ) == 2:
        return 4
    # check one pair
    for i in hand:
        if hand.count(i) != 1:
            return 5
    # check high card
    return 6


card_ordering = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def rank_with_wilds(hand_str: str):
    best_rank = 7
    for j_replace in card_ordering:
        replaced = hand_str.replace("J", j_replace)
        best_rank = min(best_rank, rank(replaced))
    return best_rank


def compare(left: str, right: str):
    left_rank, right_rank = rank_with_wilds(left), rank_with_wilds(right)
    if left_rank < right_rank:
        return 1
    if left_rank > right_rank:
        return -1

    for i in range(5):
        left_strength, right_strength = card_ordering.index(
            left[i]
        ), card_ordering.index(right[i])
        if left_strength < right_strength:
            return 1
        elif left_strength > right_strength:
            return -1
    return 0


@cmp_to_key
def compare_key(left: tuple[str, int], right: tuple[str, int]):
    return compare(left[0], right[0])


hands_ordered: list[tuple[str, int]] = sorted(hands, key=compare_key)

winnings = 0
for i, (hand, hand_bid) in enumerate(hands_ordered):
    winnings += hand_bid * (i + 1)

print(winnings)
