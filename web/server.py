import json
import string
import time
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
from planetwars.internal import better_sort_key
from planetwars.views import RealtimeView

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
            del GamesNamespace.games[self.game].sockets[id(self)]
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

    def update(self, planets, fleets):
        GamesNamespace.emit_to_game(self.game, 'update', json.dumps({
            'planets': [planet._asdict() for planet in planets],
            'fleets': [fleet._asdict() for fleet in fleets],
        }))

    def game_over(self, winner, ship_counts):
        del GamesNamespace.games[self.game]
        if self.game in games:
            del games[self.game]

@app.route('/')
def index():
    return render_template('index.html', ai_names=sorted(ai_dict.keys(), key=better_sort_key))

@app.route('/game/<path:game_id>')
def game(game_id):
    if game_id in games:
        return render_template('game.html')
    else:
        return redirect('/')

@app.route('/create-game', methods=['POST'])
def create_game():
    game_id = "".join(choice(string.lowercase) for _ in range(5))
    p1 = ai_dict[request.form["p1"]]
    p2 = ai_dict[request.form["p2"]]
    m = request.form.get("map", "map1")
    turns_per_second = float(request.form.get("tps", 2))
    smoothing_enabled = request.form.get("render") == "smooth"
    games[game_id] = PlanetWars([p1, p2], m, turns_per_second)
    view = WebsocketView(game_id)
    if smoothing_enabled:
        view = RealtimeView(30.0, turns_per_second, view)
    games[game_id].add_view(view)
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
