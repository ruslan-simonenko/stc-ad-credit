"""Partially autogenerated - edit only inside manual sections"""
from . import db
'>>> manual imports section:'
'^^^ manual imports section'

class Business(db.Model):
    __tablename__ = 'business'
    __table_args__ = (db.Index('business_uq_registration', 'registration_type', 'registration_number'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    facebook_url = db.Column(db.String(2048))
    created_by = db.Column(db.ForeignKey('user.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    registration_type = db.Column(db.String(64), nullable=False)
    registration_number = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(2048))
    user = db.relationship('User', primaryjoin='Business.created_by == User.id', backref='businesses')
    '>>> manual class code section:'
    '^^^ manual class code section'