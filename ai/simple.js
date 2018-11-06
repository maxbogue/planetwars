const partition = require('lodash/partition');

const { Order } = require('../dataTypes');
const { aggroPartition, getShips, turnDist } = require('../utils');
const { max, min, randomChoice } = require('../base');

class StrongToWeak {
  play(turn, player, planets) {
    let [myPlanets, theirPlanets] = aggroPartition(player, planets);
    let myStrongest = max(myPlanets, getShips);
    let theirWeakest = min(theirPlanets, getShips);
    return [new Order(myStrongest, theirWeakest, myStrongest.ships * 0.69)];
  }
}

class Random {
  play(turn, player, planets) {
    let mine = (thing) => thing.owner === player;
    let [myPlanets, otherPlanets] = partition(planets, mine);
    let source = randomChoice(myPlanets);
    let dest = randomChoice(otherPlanets);
    return [new Order(source, dest, source.ships / 2)];
  }
}



class AllToCloseOrWeak {
  play(turn, player, planets) {
    let currentPlanet;
    let orders = [];
    let [myPlanets, theirPlanets] = aggroPartition(player, planets);
    function distTo(otherPlanet){
      return turnDist(currentPlanet,otherPlanet);
    }
    let theirWeakest = min(theirPlanets, getShips);
    myPlanets.forEach(function(planet) {
      currentPlanet = planet;
      if (Math.random() > 0.5) {
        let closest = min(theirPlanets, distTo);
        orders.push(new Order(planet, closest, planet.ships * 0.75));
      } else {
        orders.push(new Order(planet, theirWeakest, planet.ships * 0.75));
      }
    });

    return orders;
  }
}

module.exports = { Random, StrongToWeak, AllToCloseOrWeak };


