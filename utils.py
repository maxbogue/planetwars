from collections import defaultdict
from math import ceil, sqrt

def euclidean_distance(x, y):
    return sqrt(x * x + y * y)

def dist(p1, p2):
    return euclidean_distance(p1.x - p2.x, p1.y - p2.y)

def turn_dist(p1, p2):
    return ceil(dist(p1, p2))

def get_ships(planet_or_fleet):
    return planet_or_fleet.ships

def get_growth(planet):
    return planet.growth

def partition(predicate, ls):
    yes = []
    no = []
    for e in ls:
        if predicate(e):
            yes.append(e)
        else:
            no.append(e)
    return yes, no

def aggro_partition(player_id, planets):
    mine = []
    theirs = []
    neutral = []
    for planet in planets:
        if planet.owner == player_id:
            mine.append(planet)
        elif planet.owner == 0:
            neutral.append(planet)
        else:
            theirs.append(planet)
    return mine, theirs, neutral

def battle(planet, fleets):
    """Calculates the result of the given fleets battling at the given planet.

    Note that this does not take into account the destination of the fleets,
    or their remaining travel time.

    Arguments:
        planet - The planet the fleets will fight at.
        fleets - The fleets that will take part in the battle.

    Returns:
        new_owner, new_ships

    """
    ship_counter = defaultdict(int)
    ship_counter[planet.owner] += planet.ships
    for fleet in fleets:
        ship_counter[fleet.owner] += fleet.ships
    forces = sorted(ship_counter.items(), key=lambda p: p[1], reverse=True)
    if len(forces) == 1:
        return forces[0]
    else:
        ships = forces[0][1] - forces[1][1]
        owner = planet.owner
        if ships > 0:
            # There was actually a change of owner.
            owner = forces[0][0]
        return owner, ships
