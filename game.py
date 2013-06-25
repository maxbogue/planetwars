import time
from collections import defaultdict, namedtuple
from math import ceil
from threading import Event, Thread

from planetwars.io import load_map
from planetwars.utils import dist, partition
from planetwars import Fleet, Planet

FRAMES_PER_SECOND = 30
TURNS_PER_SECOND = 100

SECONDS_PER_TURN = 1.0 / TURNS_PER_SECOND
#FRAMES_PER_TURN = ceil(FRAMES_PER_SECOND / TURNS_PER_SECOND)
#SECONDS_PER_FRAME = SECONDS_PER_TURN / FRAMES_PER_TURN

def neutral_player(pid, planets, fleets):
    return []

class PlanetWars:

    def __init__(self, players, map_name):
        if len(players) < 2:
            raise Exception("A game requires at least two players.")
        self.players = [neutral_player] + players
        self.planets, self.fleets = load_map("maps/" + map_name + ".txt")
        self.views = []
        #self.frame_renderer = Thread(target=self.frame_thread)
        #self.frame_renderer.start()

    def add_view(self, view):
        self.views.append(view)

    def freeze(self):
        planets = tuple(planet.freeze() for planet in self.planets)
        fleets = tuple(fleet.freeze() for fleet in self.fleets)
        return planets, fleets

    def play(self):
        winner = -1
        next_turn = time.time() + SECONDS_PER_TURN
        while winner < 0:
            # Do the turn
            self.do_turn()
            # Check for winner
            winner = self.check_endgame()
            # Wait until time has passed
            now = time.time()
            if now < next_turn:
                time.sleep(next_turn - now)
            next_turn += SECONDS_PER_TURN
            # Update views
            planets, fleets = self.freeze()
            for view in self.views:
                view(planets, fleets)

    def do_turn(self):
        """Performs a single turn of the game."""

        # Get orders
        planets, fleets = self.freeze()
        player_orders = [player(i, planets, fleets) for i, player in enumerate(self.players)]

        # Departure
        for player, orders in enumerate(player_orders):
            for order in orders:
                self.issue_order(player, order)

        # Advancement
        for planet in self.planets:
            planet.generate_ships()
        for fleet in self.fleets:
            fleet.advance()

        # Arrival
        arrived_fleets, self.fleets = partition(lambda fleet: fleet.has_arrived(), self.fleets)
        #print("# arrived: %d, # left: %d" % (len(arrived_fleets), len(self.fleets)))
        for planet in self.planets:
            planet.battle([fleet for fleet in arrived_fleets if fleet.destination == planet])

    def issue_order(self, player, order):
        if order.source.owner != player:
            raise Exception("Cheating!")
        ships = min(order.ships, order.source.ships)
        if ships > 0:
            source = self.planets[order.source.id]
            destination = self.planets[order.destination.id]
            source.ships -= ships
            self.fleets.append(Fleet(player, ships, source, destination))

    def check_endgame(self):
        players = range(len(self.players))[1:]
        living, dead = partition(self.is_alive, players)
        if not living:
            return 0
        elif len(living) == 1:
            return living[0]
        else:
            return -1

    def is_alive(self, player):
        for planet in self.planets:
            if planet.owner == player:
                return True
        #for fleet in self.fleets:
            #if fleet.owner == player:
                #return True
        return False
