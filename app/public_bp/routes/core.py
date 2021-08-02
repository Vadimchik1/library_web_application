from flask import render_template, make_response, url_for, request, session, redirect
from app.public_bp import blueprint
from app.models import Record, Menu, db, SubMenu, Partners, FastAccess, Contacts, WorkHours
from flask_babel import get_locale, _
import datetime
from loguru import logger


def normalize_date(html_date: str):
    date: list = html_date.split('-')
    date_list = [int(item) for item in date]
    python_date = datetime.date(date_list[0], date_list[1], date_list[2])
    return python_date


@blueprint.route('/partner_img/<id>')
@logger.catch()
def partner_img(id):
    img = Partners.query.get(id).image
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@blueprint.route('/language/<language>')
@logger.catch()
def set_language(language=None, url=None):
    session['language'] = language
    return redirect(url_for('public.index'))


@blueprint.route('/')
@blueprint.route('/index')
@logger.catch()
def index():
    title = _('Главная')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    records = Record.query.order_by(Record.created_at.desc())
    pages = records.paginate(page=page, per_page=4)

    partners = Partners.query.all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    menu = db.session.query(Menu).order_by(Menu.index).all()

    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()

    return render_template('public_bp/public_category.html', records=records, menu=full_nav, partners=partners,
                           fast_access=fast_access, pages=pages, locale=str(get_locale()), title=title,
                           contacts=contacts, work_hours=work_hours)
