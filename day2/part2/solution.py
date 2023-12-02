with open("input.txt") as f:
    power_sum = 0

    for line in f.readlines():
        game, subsets = line.split(":")
        game = game.removeprefix("Game ")
        game_id = int(game)

        red_needed = 0
        green_needed = 0
        blue_needed = 0

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

            red_needed = max(red_needed, red)
            green_needed = max(green_needed, green)
            blue_needed = max(blue_needed, blue)

        power = red_needed * green_needed * blue_needed
        power_sum += power

print(power_sum)


