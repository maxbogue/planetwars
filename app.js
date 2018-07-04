var fs = require('fs');
var bodyParser = require('body-parser')
const express = require('express')
const app = express()
app.set('views', __dirname + '/views');
app.set('view engine', 'nunjs');
app.use(bodyParser())


var datatest = {players: ["alice", "bob"] ,planets: "foo, bar, baz", turnsPerSecond: "2",map: "map1"};

server = require('http').Server(app);
var io = require('socket.io')(server);

const { PlanetWars } = require('./game');
const { TextView } = require('./views');

let game = new PlanetWars(process.argv.slice(2), 'map1', 100);
game.addView(new TextView());
game.play();


games = ['foo', 'bar']
app.get('/', function(req, res) {
    res.render('index')
})
app.get('/game/:gameID', function(req, res) {
    if (games.includes(req.params.gameID)) {
        res.render("game", {
            gameID: req.params.gameID
        })
    } else {
        res.redirect('/')
    }
})
app.use("/static", express.static('static'))
app.post('/create-game', function(req, res) {
    //res.send(req.params)
    res.send(req.body)



})

// ...elsewhere, in your app




var game_conn = io
  .of('/game')
  .on('connection', function (socket) {
//console.log(socket)
//})
//game.on('join',function (socket){ 
socket.emit('initialize',datatest)
})





function load_map(map_file) {
    var planets = []
    var fleets = []
    var mapData
    fs.readFile('./maps/' + map_file, function(err, data) {
        mapData = data
    })

}

function init_game(players, map_name, turns_per_second) {
    if (players.length() < 2) {
        throw Error("not enough players")
    }
    var player_names = players
    var turn = 0
    turn_duration = 1.0 / turns_per_second
}

server.listen(4200, () => console.log('planetwars revamped listening on port 4200!'))
