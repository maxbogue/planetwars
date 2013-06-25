from planetwars import PlanetWars
from planetwars.ai import random_ai

def text_view(planets, fleets):
    print("Planets:")
    for planet in planets:
        print("%d: %d" % (planet.owner, planet.ships))
    print("Fleets: %d" % len(fleets))

def main():
    game = PlanetWars([random_ai, random_ai], "map1")
    game.add_view(text_view)
    game.play()

if __name__ == '__main__':
    main()
