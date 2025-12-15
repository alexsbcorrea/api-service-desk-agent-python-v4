import uuid
from sqlalchemy import UUID
from datetime import datetime
from app.database.db import db
from app.models.user import User
from app.models.operator import Operator
from sqlalchemy.orm import object_session

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=False)
    id_thread = db.Column(UUID(as_uuid=True), db.ForeignKey('threads.id'), nullable=False)
    id_sender = db.Column(UUID(as_uuid=True), nullable=False)
    type_sender = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    thread = db.relationship('Thread', backref=db.backref('messages', lazy=True))
    
    @property
    def sender_name(self):
        session = object_session(self)

        if self.type_sender == 'user':
            return session.query(User.name).filter_by(id=self.id_sender).scalar()

        if self.type_sender == 'operator':
            return session.query(Operator.name).filter_by(id=self.id_sender).scalar()

        return None

    def __repr__(self):
        return f'<Message {self.id}>'