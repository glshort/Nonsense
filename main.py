from flask import Flask, request, send_file
from flask_socketio import SocketIO, emit
import logging
from Player import Player

server = Flask(__name__, static_url_path='/static')

socketio = SocketIO(server)

players = {}


def emit_status(message):
    emit('status', message, broadcast=True)


@server.route('/')
@server.route('/index.html')
def send_index():
    return send_file('static/index.html')


@socketio.on('connect')
def connect():
    logging.debug(f'{request.sid} connected')
    players[request.sid] = Player()


@socketio.on('disconnect')
def disconnect():
    logging.debug(f'{request.sid} disconnected')
    if players[request.sid].name is not None:
        emit_status(f'{players[request.sid].name} disconnected')


@socketio.on('set_name')
def set_name(name):
    player = players[request.sid]
    if player.name is None:
        emit_status(f'{name} connected')
    elif player.name != name:
        emit_status(f'{player.name} is now known as {name}')
    player.name = name


@socketio.on('chat')
def handle_chat(message):
    player = players[request.sid]
    logging.debug(f'{player.name}: {message}')
    emit_status(f'{player.name}: {message}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # enable debugging output
    server.debug = True
    socketio.run(server)
