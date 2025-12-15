from flask import Blueprint, request, jsonify
from app.models.thread import Thread
from app.models.preservice import PreService
from app.models.message import Message
from app.database.db import db
import uuid
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

thread_bp = Blueprint('thread_bp', __name__)

@thread_bp.route('/threads', methods=['POST'])
def create_thread():
    data = request.get_json()
    if not data or not 'id_preservice' in data or not 'id_user' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    new_thread = Thread(
        id_preservice=data['id_preservice'],
        id_user=data['id_user'],
        id_operator=data['id_operator']
    )
    db.session.add(new_thread)
    db.session.commit()
    
    # Finalizando o pré atendimento
    ps = PreService.query.get(data['id_preservice'])
    if not ps:
        return jsonify({'message': 'PreService not found'}), 404
    ps.active = False
    db.session.commit()
    # Finalizando o pré atendimento
    
    # Enviando mensagem inicial
    new_message = Message(
        content=data['content'],
        id_thread=new_thread.id,
        id_sender=data['id_user'],
        type_sender=data['type_sender']
    )
    db.session.add(new_message)
    db.session.commit()
    # Enviando mensagem inicial

    return jsonify({'id_thread': new_thread.id}), 201

@thread_bp.route('/threads', methods=['GET'])
def get_threads():
    threads = Thread.query.options(selectinload(Thread.user),selectinload(Thread.operator)).all()
    return jsonify([{'id': str(t.id), 'id_preservice': str(t.id_preservice), 'id_user': str(t.id_user), 'id_operator': str(t.id_operator), 'user': str(t.user.name), 'operator': str(t.operator.name)} for t in threads])

@thread_bp.route('/threads/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    t = Thread.query.options(selectinload(Thread.user),selectinload(Thread.messages)).get(thread_id)
    messages_data = []
    if len(t.messages) > 0:
        messages_data = list(map(lambda x: {'id': x.id, 'content': x.content, 'name': x.sender_name}, t.messages))
    else:
        messages_date = []
    if t:
        return jsonify({'id': str(t.id), 'id_preservice': str(t.id_preservice), 'id_user': str(t.id_user), 'user': str(t.user.name), 'messages': messages_data})
    return jsonify({'message': 'Thread not found'}), 404

@thread_bp.route('/threads/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    t = Thread.query.get(thread_id)
    if not t:
        return jsonify({'message': 'Thread not found'}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Thread deleted successfully'})
