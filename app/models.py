# -*- coding: utf-8 -*-
from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BLOB, TEXT, PickleType
from flask_user import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False, server_default='')
    active = Column(Boolean(), nullable=False, server_default='0')
    email = Column(String(255), unique=True)
    confirmed_at = Column(DateTime())

    roles = db.relationship('Role', secondary='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Record(db.Model):
    __tablename__ = 'records'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    photo = Column(BLOB)
    description = Column(TEXT)
    text = Column(TEXT)
    category_id = Column(Integer(), db.ForeignKey('categories.id'))
    created_at = Column(DateTime(), default=datetime.utcnow())


class Category(db.Model):  #
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False, unique=True)


class SubMenu(db.Model):
    __tablename__ = 'submenu'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=True)
    url_is_inner = Column(Boolean(), default=True)
    index = Column(Integer, default=None)
    menu_parent_id = Column(Integer(), db.ForeignKey('menu.id'))


class Menu(db.Model):
    __tablename__ = 'menu'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=True)
    url_is_inner = Column(Boolean, default=True)
    is_parent = Column(Boolean, default=True)
    index = Column(Integer, default=None)
    massiv_id = Column(PickleType(), default=None)


class RightPanel(db.Model):
    __tablename__ = 'right_panel'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)


class Partners(db.Model):
    __tablename__ = 'partners'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    image = Column(BLOB, nullable=False)
