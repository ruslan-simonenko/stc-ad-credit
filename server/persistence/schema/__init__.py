# DO NOT EDIT - autogenerated file. See database-gen project for details
# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CarbonAuditor(db.Model):
    __tablename__ = 'carbon_auditor'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    picture_url = db.Column(db.String(2048))


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    name = db.Column(db.String(256))
    avatar_url = db.Column(db.String(2048))


class UserRole(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.ForeignKey('role.id'), nullable=False)

    role = db.relationship('Role', primaryjoin='UserRole.role_id == Role.id', backref='user_roles')
    user = db.relationship('User', primaryjoin='UserRole.user_id == User.id', backref='user_roles')