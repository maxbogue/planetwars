from collections import defaultdict

from planetwars import PlanetWars
from planetwars.ai import random_ai
from planetwars.utils import partition

class TextView():

    def __init__(self):
        self.old_planets = None

    def print_planet(self, planet, fleets):
        def is_dest(fleet):
            return fleet.destination == planet.id
        def mine(x):
            return fleet.owner == planet.owner
        fleets = list(filter(is_dest, fleets))
        old_planet = self.old_planets[planet.id]
        owner = "N " if planet.owner == 0 else "P%d" % planet.owner
        ships = "x%d" % planet.ships
        if planet.owner != old_planet.owner:
            owner += " (was P%d)" % old_planet.owner
        elif planet.ships != old_planet.ships:
            ships += " (%+d)" % (planet.ships - old_planet.ships)
        print("#%02d: %s %s" % (planet.id, owner, ships))
        by_remaining = defaultdict(list)
        for fleet in fleets:
            by_remaining[fleet.remaining_turns].append(fleet)
        for r in sorted(by_remaining.iterkeys()):
            friends, enemies = partition(mine, by_remaining[r])
            friends_sum = sum(fleet.ships for fleet in friends)
            enemies_sum = sum(fleet.ships for fleet in enemies)
            if friends_sum > 0 and enemies_sum > 0:
                print("  ..in %d: +%d, -%d" % (r, friends_sum, enemies_sum))
            elif friends_sum > 0:
                print("  ..in %d: +%d" % (r, friends_sum))
            else:
                print("  ..in %d: -%d" % (r, enemies_sum))

    def update(self, planets, fleets):
        if not self.old_planets:
            self.old_planets = planets
        print("\nPlanets:")
        for planet in planets:
            self.print_planet(planet, fleets)
        self.old_planets = planets

def main():
    game = PlanetWars([random_ai, random_ai], "map1")
    game.add_view(TextView())
    game.play()

if __name__ == '__main__':
    main()
