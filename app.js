const bodyParser = require('body-parser');
const _ = require('lodash');
const express = require('express');

const baseUtil = require('./base');
const { PlanetWars, MAPS, AIS } = require('./game');
const { WebsocketView } = require('./socketview');

const app = express();
app.set('views', __dirname + '/views');
app.set('view engine', 'nunjs');
app.use(bodyParser());
const server = require('http').Server(app);
const io = require('socket.io')(server);
const games = {};

// publish static files
app.use('/static', express.static('static'));

// render game setup view
app.get('/', function(req, res) {
  res.render('index', {
    'map_names': _.keys(MAPS),
    'ai_names': _.keys(AIS)
  });
});

// render gameplay view
app.get('/game/:gameId', function(req, res) {
  if (games[req.params.gameId]) {
    res.render('game', {
      gameId: req.params.gameId
    });
  } else {
    res.redirect('/');
  }
});

// handle game creation
app.post('/create-game', function(req, res) {
  let gameId = baseUtil.gameId();
  let p1 = req.body.p1;
  let p2 = req.body.p2;
  let m = req.body.map;
  if (m === 'Random') {
    m = baseUtil.randomChoice(_.keys(MAPS));
  }
  let turnsPerSecond = req.body.tps;
  games[gameId] = new PlanetWars([p1, p2], m, turnsPerSecond);
  res.redirect('/game/' + gameId);
});

// tell those sockets what they want to hear
io.of('/game').on('connection', function(socket) {
  socket.on('join', function (data) {
    let view = new WebsocketView(socket);
    games[data].addView(view);
    if (games[data].views.length === 1) {
      games[data].play();
    }
  });
});

server.listen(4200);
