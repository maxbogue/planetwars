from planetwars import PlanetWars
from planetwars.ai import *
from planetwars.views import TextView

def main():
    import sys
    p1 = ai_dict[sys.argv[1]]
    p2 = ai_dict[sys.argv[2]]
    game = PlanetWars([p1, p2], "map1", 100)
    game.add_view(TextView())
    game.play()

if __name__ == '__main__':
    main()
