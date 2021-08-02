from flask import render_template, redirect, request, flash, url_for
from app.models import db, Questions, Partners, Menu, FastAccess, Contacts, WorkHours, SubMenu
from app.public_bp import blueprint
from flask_babel import get_locale, _
from loguru import logger


@blueprint.route('/contact_us', methods=['GET', 'POST'])
@logger.catch()
def contact_us():
    title = _('Виртуальная справочная служба')
    partners = Partners.query.all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    themes = ['Систематизация статей (УДК, МРНТИ', 'Электронная доставка статей)',
              '	Систематизация учебно – методических пособий (УДК, ББК)',
              'Электронная доставка документов (15% от выбранного издания)',
              'Удаленный доступ к зарубежным информационным ресурсам']
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()
    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    if request.method == 'POST':
        theme = request.form['theme']
        email = request.form['email']
        text = request.form['question']
        question = Questions(theme=theme, email=email, text=text)
        db.session.add(question)
        db.session.commit()
        flash('Отправлено')
        return redirect(url_for('public.contact_us'))
    return render_template('public_bp/contact_us.html', title=title, menu=full_nav, partners=partners,
                           fast_access=fast_access, themes=themes,
                           locale=str(get_locale()), contacts=contacts, work_hours=work_hours)
