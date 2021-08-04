from flask import render_template, make_response
from app.models import db, Record, Partners, Menu, FastAccess, Contacts, WorkHours, SubMenu
from app.public_bp import blueprint
from flask_babel import get_locale
from loguru import logger


@blueprint.route('/record/<id>', methods=['GET', 'POST'])
@logger.catch()
def show_record(id):
    record = Record.query.filter_by(id=id).first()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    partners = Partners.query.all()
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()
    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    resp = make_response(
        render_template('public_bp/public_record.html', record=record, menu=full_nav, partners=partners,
                        fast_access=fast_access, locale=str(get_locale()), title=record, contacts=contacts,
                        work_hours=work_hours))
    resp.headers['Content-Type'] = 'text/html'
    return resp


@blueprint.route('/record_img/<id>')
@logger.catch()
def record_img(id):
    img = Record.query.get(id).photo
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h
