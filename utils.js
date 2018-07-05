const sortBy = require('lodash/sortBy');

function euclideanDist(x, y) {
  return Math.sqrt(x * x + y * y);
}

function turnDist(p1, p2) {
  return Math.ceil(euclideanDist(p1.x - p2.x, p1.y - p2.y));
}

function getShips(thing) {
  return thing.ships;
}

function countShips(planets, fleets) {
  // TODO: Don't assume two players.
  let shipCounts = [0, 0, 0];
  for (let planet of planets) {
    if (!shipCounts[planet.owner]) {
      shipCounts[planet.owner] = planet.ships;
    } else {
      shipCounts[planet.owner] += planet.ships;
    }
  }
  for (let fleet of fleets) {
    if (!shipCounts[fleet.owner]) {
      shipCounts[fleet.owner] = fleet.ships;
    } else {
      shipCounts[fleet.owner] += fleet.ships;
    }
  }
  let countPairs = shipCounts.map((c, i) => [i, c]).filter(([p, c]) => c > 0);
  return sortBy(countPairs, ([p, c]) => -c);
}

function battle(planet, fleets) {
  let forces = countShips([planet], fleets);
  if (forces.length === 1) {
    return forces[0];
  }
  let ships = forces[0][1] - forces[1][1];
  let owner = planet.owner;
  if (ships > 0) {
    owner = forces[0][0];
  }
  return [owner, ships];
}

function aggroPartition(player, planets) {
  let mine = [];
  let theirs = [];
  let neutral = [];
  for (let planet of planets) {
    if (planet.owner === player) {
      mine.push(planet);
    } else if (planet.owner === 0) {
      neutral.push(planet);
    } else {
      theirs.push(planet);
    }
  }
  return [mine, theirs, neutral];
}

module.exports = { aggroPartition, battle, countShips, getShips, turnDist };
