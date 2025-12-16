from flask_socketio import SocketIO, emit, join_room
from flask import Flask, request

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on("connect")
def handle_connect(auth):
    print("Client connected")
    
    token = request.args.get('token')
    room = request.args.get('room')
    id = request.args.get('id')
    name = request.args.get('name')
    email = request.args.get('email')
    profile = request.args.get('profile')
    
    join_room(room)
    
