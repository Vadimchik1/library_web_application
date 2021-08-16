from flask import render_template, request, current_app, redirect, url_for, flash
from app.admin_bp import blueprint
from app.models import db, Role, User
from flask_user import PasswordManager, roles_required
from loguru import logger


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index')
@roles_required('admin')
@logger.catch()
def index():
    employees = User.query.all()
    return render_template('index.html', employees=employees)


@blueprint.route('/insert', methods=['GET', 'POST'])
@roles_required('admin')
@logger.catch()
def insert_user():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        password_manager = PasswordManager(current_app)
        user = User(username=username,
                    password=password_manager.hash_password(password), active=1)
        user.roles = [Role.query.filter_by(name='editor').first()]
        db.session.add(user)
        db.session.commit()
        flash('Сотрудник был успешно добавлен')
        return redirect(url_for('admin.index'))


@blueprint.route('/update', methods=['GET', 'POST'])
@roles_required('admin')
@logger.catch()
def update_user():
    if request.method == 'POST':
        user = User.query.get(request.form.get('id'))
        password_manager = PasswordManager(current_app)
        user.username = request.form['name']
        user.password = password_manager.hash_password(request.form['password'])
        user.roles = [Role.query.filter_by(name='editor').first()]
        db.session.add(user)
        db.session.commit()
        flash("Информация о сотруднике была успешно изменена")
        return redirect(url_for('admin.index'))


@blueprint.route('/delete/<id>/', methods=['GET', 'POST'])
@roles_required('admin')
@logger.catch()
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("Сотрудник был успешно удален")
    return redirect(url_for('admin.index'))
