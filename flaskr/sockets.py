from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_socketio import SocketIO, Namespace, send, emit, join_room, leave_room
import flaskr.db as db

socketio = SocketIO()

class MyNamespace(Namespace):
    def on_connect(self):
        print('Client connected')

    def on_disconnect(self):
        print('Client disconnected')

    def on_joinChatRoom(self, data):
        print(data)
        join_room(data['room'])
        emit('join', { 'room': data['room'] })

    def on_leave(self, data):
        username = data['username']
        room = data['room']
        leave_room(room)
        send(username + ' has left the room.', to=room)

    def on_chat(self, data):
        print(data)
        recordMessage(data['room'], data['sender'], data['addresse'], data['message'])
        emit('chat', { 'message': data['message'], 'sender': data['sender'] }, to=data['room'], broadcast = True)

socketio.on_namespace(MyNamespace('/socket'))

def recordMessage(room, sender, addresse, message):
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute(
            "INSERT INTO mensajes VALUES(default, %s, %s, %s, %s)",
            (room, sender, addresse, message),
        )
        connDB.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        db.close_db()
