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

boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

for part in parts:
    if "=" in part:
        label, focus_str = part.split("=")
        focus = int(focus_str)
        box = boxes[HASH(label)]

        for i, (lens_label, lens_focus) in enumerate(box):
            if lens_label == label:
                # update the focus of the existing lens
                box[i] = (label, focus)
                break
        else:
            # insert the new lens
            box.append((label, focus))

    elif "-" in part:
        label = part.removesuffix("-")
        box = boxes[HASH(label)]

        for i, (lens_label, lens_focus) in enumerate(box):
            if lens_label == label:
                # remove that lens from the box
                del box[i]
                break
        else:
            # no lens in box? nothing happens
            pass

    else:
        raise ValueError(part)

power = 0
for i, box in enumerate(boxes):
    for j, (label, focus) in enumerate(box):
        power += (i + 1) * (j + 1) * focus

print(power)
