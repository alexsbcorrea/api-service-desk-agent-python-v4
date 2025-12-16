from flask import Blueprint, request, jsonify
from app.models.message import Message
from app.database.db import db
import uuid
from app.socketio.events import socketio

message_bp = Blueprint('message_bp', __name__)

@message_bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or not 'content' in data or not 'id_thread' in data or not 'id_sender' in data or not 'type_sender' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    new_message = Message(
        content=data['content'],
        id_thread=data['id_thread'],
        id_sender=data['id_sender'],
        type_sender=data['type_sender']
    )
    db.session.add(new_message)
    db.session.commit()
    
    #Event
    socketio.emit("new_message", {'id_thread': data['id_thread']},to=f"bp-chat-{data['id_thread']}")
    #Event
    
    return jsonify({'message': 'Message created successfully'}), 201

@message_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'id': str(m.id), 'content': m.content, 'id_thread': str(m.id_thread), 'id_user': str(m.id_user)} for m in messages])

@message_bp.route('/messages/<message_id>', methods=['GET'])
def get_message(message_id):
    m = Message.query.get(message_id)
    if m:
        return jsonify({'id': str(m.id), 'content': m.content, 'id_thread': str(m.id_thread), 'id_user': str(m.id_user)})
    return jsonify({'message': 'Message not found'}), 404

@message_bp.route('/messages/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    m = Message.query.get(message_id)
    if not m:
        return jsonify({'message': 'Message not found'}), 404
    db.session.delete(m)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'})
