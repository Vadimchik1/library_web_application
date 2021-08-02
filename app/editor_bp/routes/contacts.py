from flask import render_template, redirect, url_for, flash, request
from app.editor_bp import blueprint
from app.models import db, Contacts

from flask_user import roles_required
from loguru import logger


@blueprint.route('/contacts/', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
# @logger.catch()
def contacts():
    title = 'Изменение контактных данных.'
    contact = Contacts.query.first()
    if request.method == 'POST':
        contact.address = request.form['address']
        contact.address_en = request.form['address_en']
        contact.address_kz = request.form['address_kz']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        db.session.add(contact)
        db.session.commit()
        flash('Контактные данные были успешно изменены')
        return redirect(url_for('editor.contacts'))
    return render_template('editor_bp/contacts.html', contact=contact, title=title)
