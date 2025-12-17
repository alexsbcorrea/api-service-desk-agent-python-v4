from flask_socketio import SocketIO, emit, join_room
from flask import Flask, jsonify, request
from app.database.db import db
from app.models.message import Message

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

@socketio.on("new_message")
def handle_message(data):
    content = data.get('content')
    id_sender = data.get('id_sender')
    name = data.get('name')
    id_thread = data.get('id_thread')
    type_sender = data.get('type_sender')
    room = data.get('room')
    
    print("Conteúdo",content)
    print("ID Sender",id_sender)
    print("Name",name)
    print("ID Thread",id_thread)
    print("Type Sender",type_sender)
    print("Sala", room)
    
    join_room(room)
    
    new_message = Message(
        content=content,
        id_thread=id_thread,
        id_sender=id_sender,
        type_sender=type_sender,
    )
    db.session.add(new_message)
    db.session.commit()
    
    dataObj = {
        'id': str(new_message.id),
        'content': content,
        'id_thread': str(id_thread),
        'id_user': str(id_sender),
        'name': name,
        'profile': type_sender,
        'created_at': str(new_message.created_at),   
        'updated_at': str(new_message.updated_at)   
    }
    
    socketio.emit("new_message",dataObj,to=f"bp-chat-{id_thread}")
