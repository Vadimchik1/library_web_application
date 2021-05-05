from flask import render_template, request, current_app, redirect, url_for, flash
from app.admin_bp import blueprint
from app.models import db, Role, User
from flask_user import PasswordManager, roles_required


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index')
@roles_required('admin')
def index():
    employees = User.query.all()
    return render_template('index.html', employees=employees)


@blueprint.route('/insert', methods=['GET', 'POST'])
@roles_required('admin')
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
        flash('Employee inserted successfully')
        return redirect(url_for('admin.index'))


@blueprint.route('/update', methods=['GET', 'POST'])
@roles_required('admin')
def update_user():
    if request.method == 'POST':
        user = User.query.get(request.form.get('id'))
        password_manager = PasswordManager(current_app)
        user.username = request.form['name']
        user.password = password_manager.hash_password(request.form['password'])
        user.roles = [Role.query.filter_by(name='editor').first()]
        db.session.add(user)
        db.session.commit()
        flash("Employee was changed successfully")
        return redirect(url_for('admin.index'))


@blueprint.route('/delete/<id>/', methods=['GET', 'POST'])
@roles_required('admin')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("Employee deleted successfully")
    return redirect(url_for('admin.index'))
