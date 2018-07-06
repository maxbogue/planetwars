const bodyParser = require('body-parser');
const express = require('express');
const app = express();
const ldKeys = require('lodash/keys');
app.set('views', __dirname + '/views');
app.set('view engine', 'nunjs');
app.use(bodyParser());
const baseUtil = require('./base');

const {WebsocketView} = require('./socketview');

const server = require('http').Server(app);
const io = require('socket.io')(server);
const { PlanetWars, MAPS, AIS } = require('./game');

const games = {};
app.get('/', function(req, res) {
  res.render('index', {
    'map_names': ldKeys(MAPS),
    'ai_names': ldKeys(AIS)
  });
});
app.get('/game/:gameID', function(req, res) {
  if (games[req.params.gameID]) {
    res.render('game', {
      gameID: req.params.gameID
    });
  } else {
    res.redirect('/');
  }
});
app.use('/static', express.static('static'));
app.post('/create-game', function(req, res) {

  let game_id = baseUtil.gameID();
  let p1 = req.body.p1;
  let p2 = req.body.p2;
  let m = req.body.map;
  if (m === 'Random') {
    m = baseUtil.randomChoice(ldKeys(MAPS));
  }
  let turns_per_second = req.body.tps;
  games[game_id] = new PlanetWars([p1, p2], m, turns_per_second);
  res.redirect('/game/' + game_id);
});





io.of('/game').on('connection', function(socket) {
  socket.on('join', function (data) {
    let view = new WebsocketView(socket);
    games[data].addView(view);
    if (games[data].views.length === 1) {
      games[data].play();
    }
  }
  );
});




server.listen(4200);
