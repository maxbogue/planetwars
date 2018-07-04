class TextView {

  constructor() {
    this.oldPlanets = null;
  }

  /*
  printPlanet(planet, fleets) {
    let mine = (fleet) => fleet.owner === planet.owner;
    fleets = fleets.filter((fleet) => fleet.destination === planet.id);
    let oldPlanet = this.oldPlanets[planet.id];
    let owner = player.owner === 0 ? 'N ' : `P${planet.owner}`;
    let ships = `x${planet.ships}`;
    if (planet.owner !== oldPlanet.owner) {
      owner += ` (was P${oldPlanet.owner}`;
    } else if (planet.ships !== oldPlanet.ships) {
      ships += ` (${planet.ships - oldPlanet.ship}`;
    }
    console.log("#%02d: %s %s", planet.id, owner, ships);
  }
  */

  initialize(turnsPerSecond, planets, mapName, players) {
    //console.log(turnsPerSecond, planets, mapName, players);
  }

  update(planets, fleets) {
    //console.log('update', planets, fleets);
  }

  gameOver(winner, shipCounts) {
    console.log('gameOver', winner, shipCounts);
  }
}

module.exports = { TextView };
