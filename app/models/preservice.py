import uuid
from sqlalchemy import UUID
from datetime import datetime
from app.database.db import db

class PreService(db.Model):
    __tablename__ = 'preservices'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    active = db.Column(db.Boolean, default=True, nullable=False)
    initial_msg = db.Column(db.Text, nullable=False)
    id_user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('preservices', lazy=True))

    def __repr__(self):
        return f'<PreService {self.id}>'