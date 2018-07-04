from planetwars.datatypes import Order
from planetwars.ai import planetwars_ai
from planetwars.ai.utils import aggro_partition, get_ships

@planetwars_ai
def max_ai(turn, pid, planets, fleets):
    my_planets, their_planets, _ = aggro_partition(pid, planets)
    my_strongest = max(my_planets, key=get_ships)
    their_weakest = min(their_planets, key=get_ships)
    return [Order(my_strongest, their_weakest, my_strongest.ships * 0.75)]
