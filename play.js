const { PlanetWars } = require('./game');
const { TextView } = require('./views');

let game = new PlanetWars(process.argv.slice(2), 'map1', 100);
game.addView(new TextView());
game.play();
