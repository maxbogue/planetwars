import json
import string
from collections import defaultdict
from flask import abort, Flask, redirect, render_template, Response, request
from gevent import monkey
from random import choice
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.server import SocketIOServer
from threading import Thread
from werkzeug.serving import run_with_reloader

from planetwars import PlanetWars
from planetwars.ai import random_ai

app = Flask(__name__)
monkey.patch_all()

games = {}

class GamesNamespace(BaseNamespace):

    sockets = {}
    games = {}

    def on_join(self, game):
        GamesNamespace.sockets[id(self)] = game
        GamesNamespace.games[game].sockets[id(self)] = self

    def disconnect(self, *args, **kwargs):
        print("Got a socket disconnection")
        if id(self) in self.sockets:
            game = GamesNamespace.sockets.pop(id(self))
            del GamesNamespace.games[game].sockets[id(self)]
        super(GamesNamespace, self).disconnect(*args, **kwargs)

    @classmethod
    def emit_to_game(self, game, event, *args):
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint="/game")
        for ns in self.games[game].sockets.itervalues():
            ns.socket.send_packet(pkt)

class WebsocketView:

    def __init__(self, game):
        self.game = game
        self.sockets = {}
        GamesNamespace.games[game] = self
        print("game added")

    def update(self, planets, fleets):
        GamesNamespace.emit_to_game(self.game, 'update', json.dumps({
            'planets': [planet._asdict() for planet in planets],
            'fleets': [fleet._asdict() for fleet in fleets],
        }))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<path:game_id>')
def game(game_id):
    if game_id in games:
        return render_template('game.html')
    else:
        abort(404)

@app.route('/create-game', methods=['POST'])
def create_game():
    game_id = "".join(choice(string.lowercase) for _ in range(5))
    print("Creating game: %s" % game_id)
    games[game_id] = PlanetWars([random_ai, random_ai], "map1")
    games[game_id].add_view(WebsocketView(game_id))
    Thread(target=games[game_id].play).start()
    return redirect("/game/" + game_id)

@app.route('/socket.io/<path:rest>')
def push_stream(rest):
    try:
        socketio_manage(request.environ, {'/game': GamesNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                         exc_info=True)
    return Response()

@run_with_reloader
def run_dev_server():
    app.debug = True
    port = 4200
    SocketIOServer(('', port), app, resource="socket.io").serve_forever()

if __name__ == "__main__":
    run_dev_server()
