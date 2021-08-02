from flask import current_app
from app import create_app
from app.models import db, Role, User, Contacts, WorkHours
from flask_user import PasswordManager

app = create_app()


@app.before_first_request
def cooking_app_bd():
    if not WorkHours.query.first():
        text = 'понедельник-пятница - с 10.00 до 19.00 суббота - с 10.00 до 17.00 воскресенье - выходной'
        work_hours = WorkHours(text=text)
        db.session.add(work_hours)
        db.session.commit()
    if not Contacts.query.first():
        address = 'г. Караганда пр. Нурсултана Назарбаева 56'
        phone = '+7(7212)56-75-98'
        email = 'library_ktu@mail.ru'
        contacts = Contacts(address=address, phone=phone, email=email)
        db.session.add(contacts)
        db.session.commit()
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
