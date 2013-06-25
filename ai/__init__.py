import random

from planetwars.datatypes import Order
from planetwars.utils import partition

def simple(pid, planets, fleets):
    def mine(x):
        return x.owner == pid
    my_planets, other_planets = partition(mine, planets)
    source = my_planets[0]
    dest = other_planets[0]
    return [Order(source, dest, source.ships / 2)]

def random_ai(pid, planets, fleets):
    def mine(x):
        return x.owner == pid
    my_planets, other_planets = partition(mine, planets)
    source = random.choice(my_planets)
    destination = random.choice(other_planets)
    return [Order(source, destination, source.ships / 2)]
