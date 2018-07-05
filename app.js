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
const PlanetWars = require('./game');

games = []
app.get('/', function(req, res) {
    res.render('index', {
        'map_names': ldKeys(PlanetWars.MAPS),
        'ai_names': ldKeys(PlanetWars.AIS)
    })
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

    game_id = baseUtil.gameID()
    p1 = req.body.p1
    p2 = req.body.p2


})

// ...elsewhere, in your app




var game_conn = io
    .of('/game')
    .on('connection', function(socket) {
        //console.log(socket)
        //})
        //game.on('join',function (socket){ 
        socket.emit('initialize', datatest)
    })





server.listen(4200, () => console.log('planetwars revamped listening on port 4200!'))
