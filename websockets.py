from flask_socketio import  SocketIO,join_room, leave_room, send , emit  ,close_room
from flask import session
socketio = SocketIO()

@socketio.on('message')
def message(data):
    print(f'\n\n{data}\n\n')
    send(data)


@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined " + data['room']}, room=data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left " + data['room']}, room=data['room'])

def close(room):
    close_room(room)