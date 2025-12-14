import uuid
from sqlalchemy import UUID
from datetime import datetime
from app.database.db import db

class Thread(db.Model):
    __tablename__ = 'threads'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_preservice = db.Column(UUID(as_uuid=True), db.ForeignKey('preservices.id'), nullable=False)
    id_user = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    preservice = db.relationship('PreService', backref=db.backref('threads', lazy=True))
    user = db.relationship('User', backref=db.backref('threads', lazy=True))

    def __repr__(self):
        return f'<Thread {self.id}>'