from flask import render_template, request, redirect, url_for, flash
from app.models import db, Partners, Menu, FastAccess, Contacts, WorkHours, SubMenu, Readers
from app.public_bp.routes.core import normalize_date
from app.public_bp import blueprint
from flask_babel import get_locale, _
from loguru import logger


@blueprint.route('/enroll', methods=['GET', 'POST'])
@logger.catch()
def enroll_in_library():
    title = _('Записаться в библиотеку')
    partners = Partners.query.all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()

    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        surname = request.form['surname']
        patronymic = request.form['patronymic']
        birth_date = normalize_date(
            request.form['birth_date'])
        reader_category = request.form['category']
        work_place = request.form['work_place']
        group = request.form['group']
        address = request.form['address']
        phone: str = request.form['phone']
        if not phone.isdigit():
            flash('Введите телефон числами')
            return redirect(url_for('public.enroll_in_library'))
        if reader_category == 'Обучающийся':
            reader = Readers(email=email, name=name, surname=surname, patronymic=patronymic, birth_date=birth_date,
                             category=reader_category, group=group, home_address=address, phone=phone)
        else:
            reader = Readers(email=email, name=name, surname=surname, patronymic=patronymic, birth_date=birth_date,
                             category=reader_category, work_place=work_place, group=group,
                             home_address=address, phone=phone)
        db.session.add(reader)
        db.session.commit()
        flash('Отправлено')
        return redirect(url_for('public.enroll_in_library'))
    return render_template('public_bp/enroll_in_library.html', title=title, menu=full_nav, partners=partners,
                           fast_access=fast_access,
                           locale=str(get_locale()), contacts=contacts, work_hours=work_hours)
