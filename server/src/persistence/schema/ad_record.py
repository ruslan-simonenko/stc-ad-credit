"""Partially autogenerated - edit only inside manual sections"""
from . import db
'>>> manual imports section:'
'^^^ manual imports section'

class AdRecord(db.Model):
    __tablename__ = 'ad_record'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.ForeignKey('business.id'), nullable=False, index=True)
    ad_post_url = db.Column(db.String(2048), nullable=False)
    created_by = db.Column(db.ForeignKey('user.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
    business = db.relationship('Business', primaryjoin='AdRecord.business_id == Business.id', backref='ad_records')
    user = db.relationship('User', primaryjoin='AdRecord.created_by == User.id', backref='ad_records')
    '>>> manual class code section:'
    '^^^ manual class code section'