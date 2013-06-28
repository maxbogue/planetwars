import math

from planetwars.utils import dist

def turn_dist(p1, p2):
    return math.ceil(dist(p1, p2))

def aggro_partition(pid, planets):
    mine = []
    theirs = []
    neutral = []
    for planet in planets:
        if planet.owner == pid:
            mine.append(planet)
        elif planet.owner == 0:
            neutral.append(planet)
        else:
            theirs.append(planet)
    return mine, theirs, neutral

def get_ships(planet_or_fleet):
    return planet_or_fleet.ships

def get_growth(planet):
    return planet.growth

