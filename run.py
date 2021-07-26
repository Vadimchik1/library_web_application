from flask import current_app
from app import create_app
from app.models import db, Role, User
from flask_user import PasswordManager

app = create_app()


@app.before_first_request
def cooking_app_bd():
    if not Role.query.filter_by(name='admin').first():
        role_admin = Role(name='admin')
        db.session.add(role_admin)
        db.session.commit()
    if not Role.query.filter_by(name='editor').first():
        role_editor = Role(name='editor')
        db.session.add(role_editor)
        db.session.commit()
    if not User.query.filter_by(username='admin').first():
        password_manager = PasswordManager(current_app)
        admin = User(username='admin', password=password_manager.hash_password('Admin123'), active=1)
        admin.roles = [Role.query.filter_by(name='admin').first()]
        admin.roles = [Role.query.filter_by(name='editor').first()]
        db.session.add(admin)
        db.session.commit()


if __name__ == '__main__':
    app.run(port=8080)
