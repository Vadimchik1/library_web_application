from flask import render_template, request, redirect, url_for
from app.models import db, Record, Partners, Menu, FastAccess, Contacts, WorkHours, SubMenu
from app.public_bp import blueprint
from flask_babel import get_locale
from loguru import logger


@blueprint.route('/search')
@logger.catch()
def search():
    q = request.args.get('q')
    if q:
        records = Record.query.filter(
            Record.name.contains(q) | Record.description.contains(q) | Record.text.contains(q)).all()
    else:
        return redirect(url_for('public.index'))

    partners = Partners.query.all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()

    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    return render_template('public_bp/search.html', records=records, records_amount=len(records), menu=full_nav,
                           partners=partners,
                           fast_access=fast_access, locale=str(get_locale()), contacts=contacts, work_hours=work_hours)
