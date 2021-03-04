from flask_socketio import  SocketIO,join_room, leave_room, send , emit
from flask import session
socketio = SocketIO()


@socketio.on("my event")
def handle_my_event(data):
    print(f"my event received: {data}")
    emit(data)

@socketio.on("message")
def handle_message(data):
    send(data)
    print(f"received: {data}")
@socketio.on("join")
def on_join(data):
    username= session["user"]
    room = data
    join_room(room)
    send(username+ "has entered the room. " ,room=room)

@socketio.on("leave")
def on_leave(data):
    username= data["username"]
    room= data["room"]
    leave_room()
    send(username + ' has left the room.', room=room)