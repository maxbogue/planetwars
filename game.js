const cloneDeep = require('lodash/cloneDeep');

const { Fleet, Order, Planet } = require('./dataTypes');
const { battle, countShips } = require('./utils');
const { loadAllAIs, loadAllMaps } = require('./internal');

var AIS = loadAllAIs();
var MAPS = loadAllMaps();
class NeutralPlayer {
  play(turn, player, planets, fleets) {
    return [];
  }
}

class PlanetWars {
  constructor(players, mapName, turnsPerSecond=2) {
    if (players.length < 2) {
      throw new Error("A game requires at least two players.");
    }
    this.playerNames = players;
    this.players = [new NeutralPlayer()].concat(players.map((p) => new AIS[p]()));
    this.mapName = mapName;
    let [planets, fleets] = MAPS[mapName];
    this.planets = cloneDeep(planets);
    this.fleets = cloneDeep(fleets);
    this.views = [];
    this.turnsPerSecond = turnsPerSecond;
    this.turnDuration = 1 / turnsPerSecond;
    this.turn = 0;
  }

  addView(view) {
    this.views.push(view);
  }

  freeze() {
    return cloneDeep([this.planets, this.fleets]);
  }

  play() {
    for (let view of this.views) {
      view.initialize(
          this.turnsPerSecond, this.planets, this.mapName, this.playerNames);
      view.update(this.planets, this.fleets);
    }
    let nextTurn = new Date() + this.turnDuration;
    let winner = -1;
    let shipCounts = null;
    while (winner < 0) {
      // wait until nextTurn
      nextTurn += this.turnDuration;
      this.doTurn();
      for (let view of this.views) {
        view.update(this.planets, this.fleets);
      }
      [winner, shipCounts] = this.isGameOver();
    }
    for (let view of this.views) {
      view.gameOver(winner, shipCounts);
    }
  }

  doTurn() {
    const play = (player, i) => player.play(
        this.turn, i, cloneDeep(this.planets), cloneDeep(this.fleets));
    // Get orders.
    let playerOrders = this.players.map(play);
    this.turn += 1;

    // Send fleets.
    //for (let [player, orders] of playerOrders) {
    playerOrders.forEach((orders, player) => {
      for (let order of orders) {
        this.issueOrder(player, order);
      }
    });

    // Make ships.
    for (let planet of this.planets) {
      planet.generateShips();
    }

    // Advance fleets.
    for (let fleet of this.fleets) {
      fleet.advance();
    }

    let arrivedFleets = this.fleets.filter((fleet) => fleet.hasArrived());
    this.fleets = this.fleets.filter((fleet) => !fleet.hasArrived());
    for (let planet of this.planets) {
      planet.battle(
          arrivedFleets.filter((fleet) => fleet.destination === planet));
    }
  }

  issueOrder(player, order) {
    if (order.source.owner !== player) {
      throw new Error(`Player ${player} issued an order from enemy planet ${order.source.id}.`);
    }
    let source = this.planets[order.source.id];
    // Don't let a player send more ships than they have.
    let ships = Math.floor(Math.min(order.ships, source.ships));
    if (ships > 0) {
      let destination = this.planets[order.destination.id];
      source.ships -= ships;
      this.fleets.push(new Fleet(player, ships, source, destination));
    }
  }

  isGameOver() {
    let playerIds = this.players.map((p, i) => i).slice(1);
    let living = playerIds.filter((id) => this.isAlive(id));
    if (living.length === 1) {
      return [living[0], countShips(this.planets, this.fleets)];
    } else if (this.turn >= 200) {
      let shipCounts = countShips(this.planets, this.fleets);
      shipCounts = shipCounts.filter(([p, c]) => p > 0);
      let winner = shipCounts[0][1] === shipCounts[1][1] ? 0 : shipCounts[0][0];
      return [winner, shipCounts];
    }
    return [-1, []];
  }

  isAlive(playerId) {
    for (let planet of this.planets) {
      if (planet.owner === playerId) {
        return true;
      }
    }
    return false;
  }
}

module.exports = { PlanetWars, AIS, MAPS};