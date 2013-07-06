from math import ceil

from collections import namedtuple

from planetwars.utils import battle, turn_dist

ImmutablePlanet = namedtuple("ImmutablePlanet", "id, x, y, owner, ships, growth")
ImmutableFleet = namedtuple("ImmutableFleet", "owner, ships, source, destination, total_turns, remaining_turns")
Order = namedtuple("Order", "source, destination, ships")

class Planet:

    def __init__(self, id, x, y, owner, ships, growth):
        self.id = id
        self.x = x
        self.y = y
        self.owner = owner
        self.ships = ships
        self.growth = growth

    def freeze(self):
        return ImmutablePlanet(
                self.id,
                self.x,
                self.y,
                self.owner,
                int(self.ships),
                self.growth)

    def generate_ships(self):
        if self.owner > 0: # Neutral player doesn't gain ships.
            self.ships += self.growth

    def battle(self, fleets):
        self.owner, self.ships = battle(self, fleets)

class Fleet:

    def __init__(self, owner, ships, source, destination,
                 total_turns=None, remaining_turns=None):
        self.owner = owner
        self.ships = ships
        self.source = source
        self.destination = destination
        if total_turns is None:
            self.total_turns = turn_dist(source, destination)
        else:
            self.total_turns = total_turns
        if remaining_turns is None:
            self.remaining_turns = self.total_turns
        else:
            self.remaining_turns = remaining_turns

    def freeze(self):
        return ImmutableFleet(
                self.owner,
                self.ships,
                self.source.id if isinstance(self.source, Planet) else self.source,
                self.destination.id if isinstance(self.destination, Planet) else self.destination,
                self.total_turns,
                self.remaining_turns)

    def advance(self):
        self.remaining_turns -= 1

    def has_arrived(self):
        return self.remaining_turns <= 0
