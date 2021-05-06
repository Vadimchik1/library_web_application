from flask import render_template, redirect, url_for
from app.public_bp import blueprint
from app.models import Category, Record, Menu, db


@blueprint.route('/')
@blueprint.route('/index')
def index():
    records = Record.query.all()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    return render_template('public_bp/public_category.html', records=records, menu=menu)


@blueprint.route('/categories/<id>', methods=['GET', 'POST'])
def category(id):
    records = Record.query.filter_by(category_id=id).all()
    # category_name = Category.query.filter_by(id=id).first().name
    menu = db.session.query(Menu).order_by(Menu.index).all()
    print(menu)
    return render_template('public_bp/public_category.html', records=records, menu=menu)


@blueprint.route('/record/<id>', methods=['GET', 'POST'])
def show_record(id):
    record = Record.query.filter_by(id=id).first()
    return render_template('public_bp/public_record.html', record=record)
