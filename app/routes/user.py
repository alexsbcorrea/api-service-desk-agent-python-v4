from flask import Blueprint, request, jsonify
from app.models.user import User
from app.database.db import db
import uuid
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload, joinedload

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users/login', methods=['POST'])
def login_user():
    print('NOVO USUARIO')
    data = request.get_json()
    if not data or not 'email' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    email = data['email']
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'id': str(user.id), 'name': user.name, 'email': user.email, 'token': "123456789"})
    

@user_bp.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'name' in data or not 'email' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    new_user = User(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': str(user.id), 'name': user.name, 'email': user.email} for user in users])

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.options(selectinload(User.threads),selectinload(User.preservices)).get(user_id)
    
    preservice_data = list(map(lambda x: {'id': x.id, 'active': x.active}, user.preservices))
    threads_data = list(map(lambda x: {'id': x.id}, user.threads))

    if user:
        return jsonify({'id': str(user.id), 'name': user.name, 'email': user.email, 'preservices': preservice_data, 'threads': threads_data})
    return jsonify({'message': 'User not found'}), 404

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
