import time
from collections import defaultdict
from threading import Lock, Thread

from planetwars import Planet, Fleet
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
        for r in sorted(by_remaining.keys()):
            friends, enemies = partition(mine, by_remaining[r])
            friends_sum = sum(fleet.ships for fleet in friends)
            enemies_sum = sum(fleet.ships for fleet in enemies)
            if friends_sum > 0 and enemies_sum > 0:
                print("  ..in %d: +%d, -%d" % (r, friends_sum, enemies_sum))
            elif friends_sum > 0:
                print("  ..in %d: +%d" % (r, friends_sum))
            else:
                print("  ..in %d: -%d" % (r, enemies_sum))

    def initialize(self, turns_per_second, planets, map_name, players):
        print("%s on %s" % (" vs ".join(players), map_name))
        print("Running at %d turns per second" % turns_per_second)

    def update(self, planets, fleets):
        if not self.old_planets:
            self.old_planets = planets
        print("\nPlanets:")
        for planet in planets:
            self.print_planet(planet, fleets)
        self.old_planets = planets

    def game_over(self, winner, ship_counts):
        if winner > 0:
            print("Player %d wins!" % winner)
        else:
            print("Tie!")
        print("Final ship counts:")
        for player, ships in ship_counts:
            if player > 0:
                print("Player %d: % 4d" % (player, ships))

class RealtimeView:
    
    def __init__(self, frames_per_second, turns_per_second, *wrapped_views):
        self.seconds_per_frame = 1.0 / frames_per_second
        self.turns_per_frame = turns_per_second / frames_per_second
        self.wrapped_views = wrapped_views
        self.planets = []
        self.fleets = []
        self.lock = Lock()
        self.winner = -1
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        next_frame_time = time.time()
        while True:
            with self.lock:
                if self.planets:
                    planets = tuple(planet.freeze() for planet in self.planets)
                    fleets = tuple(fleet.freeze() for fleet in self.fleets)
                    for view in self.wrapped_views:
                        view.update(planets, fleets)
                    self.next_frame()
            if self.winner >= 0:
                break
            next_frame_time += self.seconds_per_frame
            sleep_duration = next_frame_time - time.time()
            if sleep_duration > 0:
                time.sleep(sleep_duration)
        for view in self.wrapped_views:
            view.game_over(self.winner, self.ship_counts)

    def next_frame(self):
        for planet in self.planets:
            if planet.owner > 0:
                planet.ships += planet.growth * self.turns_per_frame
        for fleet in self.fleets:
            fleet.remaining_turns -= self.turns_per_frame
        self.fleets = [fleet for fleet in self.fleets if fleet.remaining_turns >= 0]

    def initialize(self, *args, **kwargs):
        with self.lock:
            for view in self.wrapped_views:
                view.initialize(*args, **kwargs)

    def update(self, planets, fleets):
        with self.lock:
            self.planets = [Planet(*planet) for planet in planets]
            self.fleets = [Fleet(*fleet) for fleet in fleets]

    def game_over(self, winner, ship_counts):
        self.winner = winner
        self.ship_counts = ship_counts
