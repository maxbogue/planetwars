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
from planetwars.ai import ai_dict

app = Flask(__name__)
monkey.patch_all()

games = {}

class GamesNamespace(BaseNamespace):

    games = {}

    def on_join(self, game):
        self.game = game
        GamesNamespace.games[self.game].sockets[id(self)] = self

    def disconnect(self, *args, **kwargs):
        if hasattr(self, "game") and self.game in GamesNamespace.games:
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

    def game_over(self, winner):
        del GamesNamespace.games[self.game]
        if self.game in games:
            del games[self.game]

@app.route('/')
def index():
    return render_template('index.html', ai_names=sorted(ai_dict.keys()))

@app.route('/game/<path:game_id>')
def game(game_id):
    if game_id in games:
        return render_template('game.html')
    else:
        return redirect('/')

@app.route('/create-game', methods=['POST'])
def create_game():
    print(request.form)
    game_id = "".join(choice(string.lowercase) for _ in range(5))
    print("Creating game: %s" % game_id)
    print(request.form["p1"])
    print(request.form["p2"])
    p1 = ai_dict[request.form["p1"]]
    p2 = ai_dict[request.form["p2"]]
    games[game_id] = PlanetWars([p1, p2], "map1")
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
