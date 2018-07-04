const partition = require('lodash/partition');

const { Order } = require('../dataTypes');
const { aggroPartition, getShips } = require('../utils');
const { max, min, randomChoice } = require('../base');

class StrongToWeak {
  play(turn, player, planets, fleets) {
    let [myPlanets, theirPlanets] = aggroPartition(player, planets);
    let myStrongest = max(myPlanets, getShips);
    let theirWeakest = min(theirPlanets, getShips);
    return [new Order(myStrongest, theirWeakest, myStrongest.ships * 0.75)];
  }
}

class Random {
  play(turn, player, planets, fleets) {
    let mine = (thing) => thing.owner === player;
    let [myPlanets, otherPlanets] = partition(planets, mine);
    let source = randomChoice(myPlanets);
    let dest = randomChoice(otherPlanets);
    return [new Order(source, dest, source.ships / 2)];
  }
}

module.exports = { Random, StrongToWeak };
