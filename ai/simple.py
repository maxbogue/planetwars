import random

from planetwars.ai import planetwars_ai
from planetwars.datatypes import Order
from planetwars.utils import *

@planetwars_ai("StrongToWeak")
def strong_to_weak(turn, pid, planets, fleets):
    my_planets, their_planets, _ = aggro_partition(pid, planets)
    my_strongest = max(my_planets, key=get_ships)
    their_weakest = min(their_planets, key=get_ships)
    return [Order(my_strongest, their_weakest, my_strongest.ships * 0.75)]

@planetwars_ai("AllToWeak")
def all_to_weak(turn, pid, planets, fleets):
    my_planets, their_planets, _ = aggro_partition(pid, planets)
    destination = min(their_planets, key=get_ships)
    orders = []
    for planet in my_planets:
        orders.append(Order(planet, destination, planet.ships * 0.75))
    return orders

@planetwars_ai("AllToCloseOrWeak")
def all_to_close_or_weak(turn, pid, planets, fleets):
    my_planets, their_planets, neutral_planets = aggro_partition(pid, planets)
    other_planets = their_planets + neutral_planets
    their_weakest = min(their_planets, key=get_ships)
    my_total = sum(map(get_ships, my_planets))
    destination = min(their_planets, key=get_ships)
    orders = []
    for planet in my_planets:
        if random.random() < 0.5:
            def dist_to(other_planet):
                return turn_dist(planet, other_planet)
            closest = min(other_planets, key=dist_to)
            orders.append(Order(planet, closest, planet.ships * 0.75))
        else:
            orders.append(Order(planet, their_weakest, planet.ships * 0.75))
    return orders

@planetwars_ai("Random")
def random_ai(turn, pid, planets, fleets):
    def mine(x):
        return x.owner == pid
    my_planets, other_planets = partition(mine, planets)
    source = random.choice(my_planets)
    destination = random.choice(other_planets)
    return [Order(source, destination, source.ships / 2)]
