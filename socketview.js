class WebsocketView {

  constructor(socket) {
    this.socket = socket;
  }

  initialize(turnsPerSecond, planets, mapName, players) {
    this.socket.emit('initialize',
                     { turnsPerSecond, planets, mapName, players });
  }

  update(planets, fleets) {
    let fleetsForJson = fleets.map((fleet) => fleet.forJson());
    this.socket.emit('update', [planets, fleetsForJson]);
  }

  gameOver(winner, shipCounts) {
    this.socket.emit('gameOver', winner, shipCounts);
  }
}

module.exports = { WebsocketView };
