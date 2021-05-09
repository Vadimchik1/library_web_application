from flask import render_template, request, redirect, url_for, flash, jsonify
from app.editor_bp import blueprint
from app.models import Partners


@blueprint.route('/partners')
def show_partners():
    partners = Partners.query.all()
    return render_template('editor_bp/partners.html', partners=partners, title='Партнеры')


@blueprint.route('/add_partner', methods=['GET', 'POST'])
def add_partner():
    return render_template('editor_bp/add_partner.html', title='Добавить партнера')


@blueprint.route('/update_partner', methods=['GET', 'POST'])
def update_partner():
    pass
