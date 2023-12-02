with open("input.txt") as f:
    id_sum = 0

    for line in f.readlines():
        game, subsets = line.split(":")
        game = game.removeprefix("Game ")
        game_id = int(game)

        subsets_list = subsets.split(";")
        for subset in subsets_list:
            red = 0
            green = 0
            blue = 0

            for part in subset.split(","):
                number, color = part.strip().split(" ")
                match color:
                    case "red":
                        red += int(number)
                    case "green":
                        green += int(number)
                    case "blue":
                        blue += int(number)

            if not (red <= 12 and green <= 13 and blue <= 14):
                break
        else:
            id_sum += game_id

print(id_sum)


