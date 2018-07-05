var fs = require('fs');
var bodyParser = require('body-parser')
const express = require('express')
const app = express()
var ldKeys = require('lodash/keys')
app.set('views', __dirname + '/views');
app.set('view engine', 'nunjs');
app.use(bodyParser())
const baseUtil = require('./base')
console.log(baseUtil.gameID())

server = require('http').Server(app);
var io = require('socket.io')(server);
const { PlanetWars, MAPS, AIS } = require('./game');

const games = {}
app.get('/', function(req, res) {
    res.render('index', {
        'map_names': ldKeys(MAPS),
        'ai_names': ldKeys(AIS)
    })
})
app.get('/game/:gameID', function(req, res) {
    if (games[req.params.gameID]) {
        res.render("game", {
            gameID: req.params.gameID
        })
    } else {
        res.redirect('/')
    }
})
app.use("/static", express.static('static'))
app.post('/create-game', function(req, res) {

    game_id = baseUtil.gameID()
    p1 = req.body.p1
    p2 = req.body.p2
    m = req.body.map
    if (m == "Random") {
        m = baseUtil.randomChoice(ldKeys(MAPS))
    }
    turns_per_second = req.body.tps
    games[game_id] = new PlanetWars([p1, p2], m, turns_per_second)
    res.redirect('/game/' + game_id)
})

// ...elsewhere, in your app




var game_conn = io
    .of('/game')
    .on('connection', function(socket) {
        //console.log(socket)
        //})
        //game.on('join',function (socket){ 
    
socket.on('join', function (data) {
 var init_data = {}
init_data['turns_per_second'] = games[data].turnsPerSecond
init_data['players'] = games[data].playerNames
init_data['map'] = games[data].mapName
init_data['planets'] = games[data].planets
console.log(init_data)
socket.emit('initialize', init_data)
})})




server.listen(4200, () => console.log('planetwars revamped listening on port 4200!'))
