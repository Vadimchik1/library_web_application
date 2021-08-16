# -*- coding: utf-8 -*-
from app.extensions import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, TEXT, PickleType, Date, BLOB, LargeBinary
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
    __searchable__ = ['text']
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    name_en = Column(String(250))
    name_kz = Column(String(250))
    photo = Column(LargeBinary)
    description = Column(TEXT)
    description_en = Column(TEXT)
    description_kz = Column(TEXT)
    text = Column(TEXT)
    text_en = Column(TEXT)
    text_kz = Column(TEXT)
    category_id = Column(Integer(), db.ForeignKey('categories.id'))
    created_at = Column(DateTime(), default=datetime.utcnow())
    normal_date = Column(Date(), default=datetime.utcnow())
    url = Column(String(250))
    image = Column(LargeBinary)


class Category(db.Model):  #
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    url = Column(String(250))


class SubMenu(db.Model):
    __tablename__ = 'submenu'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    name_en = Column(String(250))
    name_kz = Column(String(250))
    url = Column(String(250), nullable=True)
    url_is_inner = Column(Boolean(), default=True)
    index = Column(Integer, default=None)
    menu_parent_id = Column(Integer(), db.ForeignKey('menu.id'))


class Menu(db.Model):
    __tablename__ = 'menu'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    name_en = Column(String(250))
    name_kz = Column(String(250))

    url = Column(String(250), nullable=True)
    url_is_inner = Column(Boolean, default=True)
    is_parent = Column(Boolean, default=True)
    index = Column(Integer, default=None)
    massiv_id = Column(PickleType(), default=None)


class FastAccess(db.Model):
    __tablename__ = 'fast_access'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    name_en = Column(String(250))
    name_kz = Column(String(250))
    url = Column(String(250), nullable=True)
    url_is_inner = Column(Boolean, default=True)
    index = Column(Integer, default=None)


class RightPanel(db.Model):
    __tablename__ = 'right_panel'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)


class Partners(db.Model):
    __tablename__ = 'partners'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    image = Column(LargeBinary, nullable=False)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer(), primary_key=True)
    theme = Column(String(300))
    email = Column(String(255))
    text = Column(TEXT)
    created_at = Column(DateTime(), default=datetime.utcnow())


class Readers(db.Model):
    __tablename__ = 'readers'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250))
    surname = Column(String(250))
    patronymic = Column(String(250))
    birth_date = Column(Date())
    category = Column(String(250))
    work_place = Column(String(250))
    group = Column(String(250))
    home_address = Column(String(250))
    phone = Column(String(30))
    email = Column(String(255), unique=True)


class NewBooks(db.Model):
    __tablename__ = 'new_books'
    id = Column(Integer(), primary_key=True)
    title = Column(String(250))
    title_en = Column(String(250))
    title_kz = Column(String(250))
    description = Column(TEXT)
    description_en = Column(TEXT)
    description_kz = Column(TEXT)
    image = Column(LargeBinary, nullable=False)
    text = Column(TEXT)
    text_en = Column(TEXT)
    text_kz = Column(TEXT)


class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = Column(Integer(), primary_key=True)
    address = Column(String(300))
    address_en = Column(String(300))
    address_kz = Column(String(300))
    phone = Column(String(30))
    email = Column(String(255))


class WorkHours(db.Model):
    __tablename__ = 'work_hours'
    id = Column(Integer, primary_key=True)
    text = Column(String(300))
    text_en = Column(String(300))
    text_kz = Column(String(300))
