
class WebsocketView {

  constructor(socket) {
    this.oldPlanets = null;
    this.socket = socket;
  }
  
  initialize(turnsPerSecond, planets, mapName, players) {
   console.log('initializing')
   this.socket.emit('initialize', {turnsPerSecond, planets, mapName, players});
  }

  update(planets, fleets) {
  this.socket.emit('update', [planets, fleets.map((fleet) => fleet.forJson())]);
  }

  gameOver(winner, shipCounts) {
    this.socket.emit('gameOver', winner, shipCounts);
    console.log('game over - '+winner+' wins.')
  }
}

module.exports = { WebsocketView };
