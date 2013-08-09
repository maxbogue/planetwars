import time
from collections import defaultdict

from planetwars import Fleet, Planet
from planetwars.internal import load_all_maps
from planetwars.utils import count_ships, partition

def _neutral_player(turn, pid, planets, fleets):
    return []

class PlanetWars:

    ais = {}
    maps = load_all_maps()

    def __init__(self, players, map_name, turns_per_second=2):
        if len(players) < 2:
            raise Exception("A game requires at least two players.")
        self.player_names = players
        self.players = [_neutral_player] + [PlanetWars.ais[player] for player in players]
        self.map_name = map_name
        planets, fleets = PlanetWars.maps[map_name]
        self.planets = [Planet(*planet) for planet in planets]
        self.fleets = [Fleet(*fleet) for fleet in fleets]
        self.views = []
        self.turns_per_second = turns_per_second
        self.turn_duration = 1.0 / turns_per_second
        self.turn = 0

    def add_view(self, view):
        self.views.append(view)

    def freeze(self):
        planets = tuple(planet.freeze() for planet in self.planets)
        fleets = tuple(fleet.freeze() for fleet in self.fleets)
        return planets, fleets

    def play(self):
        planets, fleets = self.freeze()
        for view in self.views:
            view.initialize(self.turns_per_second, self.planets, self.map_name, self.player_names)
            view.update(planets, fleets)
        next_turn = time.time() + self.turn_duration
        winner = -1
        while winner < 0:
            # Wait until time has passed
            now = time.time()
            if now < next_turn:
                time.sleep(next_turn - now)
            next_turn += self.turn_duration
            # Do the turn
            self.do_turn()
            # Update views
            planets, fleets = self.freeze()
            for view in self.views:
                view.update(planets, fleets)
            # Check for end game.
            winner, ship_counts = self.gameover()
        for view in self.views:
            view.game_over(winner, ship_counts)

    def do_turn(self):
        """Performs a single turn of the game."""

        # Get orders
        planets, fleets = self.freeze()
        player_orders = [player(self.turn, i, planets, fleets) for i, player in enumerate(self.players)]
        self.turn += 1

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
        for planet in self.planets:
            planet.battle([fleet for fleet in arrived_fleets if fleet.destination == planet])

    def issue_order(self, player, order):
        if order.source.owner != player:
            raise Exception("Player %d issued an order from enemy planet %d." % (player, order.source.id))
        source = self.planets[order.source.id]
        ships = int(min(order.ships, source.ships))
        if ships > 0:
            destination = self.planets[order.destination.id]
            source.ships -= ships
            self.fleets.append(Fleet(player, ships, source, destination))

    def gameover(self):
        players = range(1, len(self.players))
        living = list(filter(self.is_alive, players))
        if len(living) == 1:
            return living[0], count_ships(self.planets, self.fleets)
        elif self.turn >= 200:
            ship_counts = count_ships(self.planets, self.fleets)
            ship_counts = [(p, s) for p, s in ship_counts if p > 0]
            winner = 0 if ship_counts[0][1] == ship_counts[1][1] else ship_counts[0][0]
            return winner, ship_counts
        else:
            return -1, []

    def is_alive(self, player):
        for planet in self.planets:
            if planet.owner == player:
                return True
        return False
