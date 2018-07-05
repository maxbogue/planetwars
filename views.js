const _ = require('lodash');

const { getShips } = require('./utils');

class TextView {

  constructor() {
    this.oldPlanets = null;
  }

  printPlanet(planet, fleets) {
    let mine = (fleet) => fleet.owner === planet.owner;
    let oldPlanet = this.oldPlanets[planet.id];
    let owner = planet.owner === 0 ? 'N ' : `P${planet.owner}`;
    let ships = `x${planet.ships}`;
    if (planet.owner !== oldPlanet.owner) {
      owner += ` (was P${oldPlanet.owner}`;
    } else if (planet.ships !== oldPlanet.ships) {
      ships += ` (${planet.ships - oldPlanet.ship}`;
    }
    console.log(`#${planet.id}: ${owner} ${ships}`);
    let byRemaining = {};
    for (let fleet of fleets) {
      if (!byRemaining[fleet.remainingTurns]) {
        byRemaining[fleet.remainingTurns] = [];
      }
      byRemaining[fleet.remainingTurns].push(fleet);
    }
    for (let r of _.keys(byRemaining).sort()) {
      let [friends, enemies] = _.partition(byRemaining[r], mine);
      let friendShips = _.sum(friends.map(getShips));
      let enemyShips = _.sum(enemies.map(getShips));
      if (friendShips > 0 && enemyShips > 0) {
        console.log(`  ..in ${r}: +${friendShips}, -${enemyShips}`);
      } else if (friendShips > 0) {
        console.log(`  ..in ${r}: +${friendShips}`);
      } else if (enemyShips > 0) {
        console.log(`  ..in ${r}: -${enemyShips}`);
      }
    }
  }

  initialize(turnsPerSecond, planets, mapName, players) {
    console.log(`${players.join(' vs ')} on ${mapName}`);
    console.log(`Running at ${turnsPerSecond} turns per second.`);
  }

  update(planets, fleets) {
    if (!this.oldPlanets) {
      this.oldPlanets = planets;
    }
    console.log('\nPlanets:');
    for (let planet of planets) {
      this.printPlanet(planet, fleets.filter(
        (fleet) => fleet.destination === planet));
    }
    this.oldPlanets = planets;
  }

  gameOver(winner, shipCounts) {
    console.log('gameOver', winner, shipCounts);
  }
}

module.exports = { TextView };
