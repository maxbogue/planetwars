const { battle, turnDist } = require('./utils');

class Planet {
  constructor(id, x, y, owner, ships, growth) {
    this.id = id;
    this.x = x;
    this.y = y;
    this.owner = owner;
    this.ships = ships;
    this.growth = growth;
  }

  generateShips() {
    if (this.owner > 0) {
      this.ships += this.growth;
    }
  }

  battle(fleets) {
    if (fleets.length > 0) {
      [this.owner, this.ships] = battle(this, fleets);
    }
  }
}

class Fleet {
  constructor(owner, ships, source, destination, totalTurns, remainingTurns) {
    this.owner = owner;
    this.ships = ships;
    this.source = source;
    this.destination = destination;
    this.totalTurns = totalTurns || turnDist(source, destination);
    this.remainingTurns = remainingTurns || this.totalTurns;
  }

  advance() {
    this.remainingTurns -= 1;
  }

  hasArrived() {
    return this.remainingTurns <= 0;
  }
}

class Order {
  constructor(source, destination, ships) {
    this.source = source;
    this.destination = destination;
    this.ships = ships;
  }
}

module.exports = { Planet, Fleet, Order };
