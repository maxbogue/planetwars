from planetwars import Fleet, Planet

def load_map(map_file):
    planets = []
    fleets = []
    with open(map_file) as f:
        for line in f:
            line = line[:line.find("#")]
            tokens = line.split()
            if not tokens:
                continue
            elif tokens[0] == "P":
                x = float(tokens[1])
                y = float(tokens[2])
                owner = int(tokens[3])
                ships = int(tokens[4])
                growth = int(tokens[5])
                planets.append(Planet(len(planets), x, y, owner, ships, growth))
            elif tokens[0] == "F":
                owner = int(tokens[1])
                ships = int(tokens[2])
                source = int(tokens[3])
                destination = int(tokens[4])
                total_turns = int(tokens[5])
                remaining_turns = int(tokens[6])
                fleets.append(Fleet(owner, ships, source, destination,
                                    total_turns, remaining_turns))
    return planets, fleets
