"""Utility functions that are used for things besides game logic."""

import os.path
import re

import planetwars
from planetwars.datatypes import ImmutableFleet, ImmutablePlanet

MAP_DIR = os.path.join(os.path.dirname(planetwars.__file__), "maps")

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
                planets.append(ImmutablePlanet(len(planets), x, y, owner, ships, growth))
            elif tokens[0] == "F":
                owner = int(tokens[1])
                ships = int(tokens[2])
                source = int(tokens[3])
                destination = int(tokens[4])
                total_turns = int(tokens[5])
                remaining_turns = int(tokens[6])
                fleets.append(ImmutableFleet(owner, ships, source, destination,
                                    total_turns, remaining_turns))
    return planets, fleets

def load_all_maps():
    maps = {}
    for dirpath, _, filenames in os.walk(MAP_DIR):
        for filename in filenames:
            map_path = os.path.join(dirpath, filename)
            map_name = os.path.splitext(map_path[len(MAP_DIR) + 1:])[0]
            maps[map_name] = load_map(map_path)
    return maps

DIGITS = set("0123456789")
ROMAN_NUMERALS = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}

def is_digit(s):
    if len(s) == 0:
        return False
    for c in s:
        if c not in DIGITS:
            return False
    return True

def is_roman_numeral(s):
    if len(s) == 0:
        return False
    for c in s.upper():
        if c not in ROMAN_NUMERALS:
            return False
    return True

def roman_to_int(s):
    s = s.upper()
    if not is_roman_numeral(s):
        raise ValueError("Input is not a valid roman numeral: \"%s\"" % s)
    n = 0
    for i, c in enumerate(s):
        v = ROMAN_NUMERALS[c]
        if i < len(s) - 1 and ROMAN_NUMERALS[s[i + 1]] > v:
            n -= v
        else:
            n += v
    return n

def maybe_to_int(s):
    if is_digit(s):
        return int(s)
    elif is_roman_numeral(s):
        return roman_to_int(s)
    else:
        return s

def natural_key(s):
    return [maybe_to_int(t) for t in re.split("(\d+|\s+)", s)]
