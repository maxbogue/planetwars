import time
from collections import defaultdict

from planetwars.utils import count_ships, partition
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

def neutral_player(turn, pid, planets, fleets):
    return []

class PlanetWars:

    def __init__(self, players, map_name, turns_per_second=2):
        if len(players) < 2:
            raise Exception("A game requires at least two players.")
        self.players = [neutral_player] + players
        self.planets, self.fleets = load_map("maps/" + map_name + ".txt")
        self.views = []
        self.turn_duration = 1.0 / turns_per_second
        self.turn = 0

    def add_view(self, view):
        self.views.append(view)

    def freeze(self):
        planets = tuple(planet.freeze() for planet in self.planets)
        fleets = tuple(fleet.freeze() for fleet in self.fleets)
        return planets, fleets

    def play(self):
        next_turn = time.time() + self.turn_duration
        while True:
            # Do the turn
            self.do_turn()
            # Update views
            planets, fleets = self.freeze()
            for view in self.views:
                view.update(planets, fleets)
            # Check for end game.
            winner, ship_counts = self.gameover()
            if winner >= 0:
                break
            # Wait until time has passed
            now = time.time()
            if now < next_turn:
                time.sleep(next_turn - now)
            next_turn += self.turn_duration
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
        living = filter(self.is_alive, players)
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
