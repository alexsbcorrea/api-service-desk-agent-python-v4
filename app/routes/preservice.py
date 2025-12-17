from flask import Blueprint, request, jsonify
from app.models.preservice import PreService
from app.database.db import db
import uuid
from sqlalchemy.orm import joinedload
from sqlalchemy import desc, asc

preservice_bp = Blueprint('preservice_bp', __name__)

@preservice_bp.route('/preservices', methods=['POST'])
def create_preservice():
    data = request.get_json()
    if not data or not 'id_user' in data or not 'initial_msg' in data:
        return jsonify({'message': 'Missing required fields'}), 400
    new_preservice = PreService(
        id_user=data['id_user'],
        initial_msg=data['initial_msg']        
    )
    db.session.add(new_preservice)
    db.session.commit()
    return jsonify({'message': 'PreService created successfully'}), 201

@preservice_bp.route('/preservices', methods=['GET'])
def get_preservices():
    preservices = PreService.query.options(joinedload(PreService.user)).filter_by(active=True).order_by(asc(PreService.created_at)).all()
    return jsonify([{'id': str(ps.id), 'active': ps.active, 'initial_msg': str(ps.initial_msg), 'id_user': str(ps.id_user), 'user': str(ps.user.name), 'profile': str(ps.user.profile), 'created_at': str(ps.created_at), 'updated_at': str(ps.updated_at)} for ps in preservices])

@preservice_bp.route('/preservices/<preservice_id>', methods=['GET'])
def get_preservice(preservice_id):
    ps = PreService.query.get(preservice_id)
    print(ps)
    if ps:
        return jsonify({'id': str(ps.id), 'active': ps.active, 'initial_msg': str(ps.initial_msg), 'id_user': str(ps.id_user), 'user': str(ps.user.name)})
    return jsonify({'message': 'PreService not found'}), 404

@preservice_bp.route('/preservices/<preservice_id>', methods=['PUT'])
def update_preservice(preservice_id):
    ps = PreService.query.get(preservice_id)
    if not ps:
        return jsonify({'message': 'PreService not found'}), 404
    data = request.get_json()
    ps.active = data.get('active', ps.active)
    db.session.commit()
    return jsonify({'message': 'PreService updated successfully'})

@preservice_bp.route('/preservices/<preservice_id>', methods=['DELETE'])
def delete_preservice(preservice_id):
    ps = PreService.query.get(preservice_id)
    if not ps:
        return jsonify({'message': 'PreService not found'}), 404
    db.session.delete(ps)
    db.session.commit()
    return jsonify({'message': 'PreService deleted successfully'})
