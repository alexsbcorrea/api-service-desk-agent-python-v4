from flask import Blueprint, request, jsonify
from app.models.operator import Operator
from app.database.db import db
import uuid
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload, joinedload

operator_bp = Blueprint('operator_bp', __name__)

@operator_bp.route('/operators/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or not 'email' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    email = data['email']
    user = Operator.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'message': 'Operador não encontrado.'}), 404
    return jsonify({'id': str(user.id), 'name': user.name, 'email': user.email, 'profile': user.profile, 'token': "123456789"})
    

@operator_bp.route('/operators', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'name' in data or not 'email' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    new_user = Operator(
        name=data['name'],
        email=data['email'],
        profile='operator'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Operator created successfully'}), 201

@operator_bp.route('/operators', methods=['GET'])
def get_users():
    users = Operator.query.all()
    return jsonify([{'id': str(user.id), 'name': user.name, 'email': user.email} for user in users])

@operator_bp.route('/operators/<user_id>', methods=['GET'])
def get_user(user_id):
    user = Operator.query.options(selectinload(Operator.threads)).get(user_id)
    
    threads_data = list(map(lambda x: {'id': x.id}, user.threads))

    if user:
        return jsonify({'id': str(user.id), 'name': user.name, 'email': user.email, 'threads': threads_data})
    return jsonify({'message': 'Operator not found'}), 404

@operator_bp.route('/operators/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = Operator.query.get(user_id)
    if not user:
        return jsonify({'message': 'Operator not found'}), 404
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Operator updated successfully'})

@operator_bp.route('/operators/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Operator.query.get(user_id)
    if not user:
        return jsonify({'message': 'Operator not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Operator deleted successfully'})