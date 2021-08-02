from flask import render_template, make_response, request
from app.public_bp import blueprint
from app.models import Menu, db, SubMenu, Partners, FastAccess, NewBooks, \
    Contacts, WorkHours
from flask_babel import get_locale, _
from loguru import logger


@blueprint.route('/new_arrivals')
@logger.catch()
def new_arrivals():
    title = _('Новые поступления')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    books = NewBooks.query.order_by(NewBooks.id.desc())
    pages = books.paginate(page=page, per_page=4)

    partners = Partners.query.all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()

    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu

    return render_template('public_bp/public_new_arrivals.html', books=books, menu=full_nav, partners=partners,
                           fast_access=fast_access, pages=pages, locale=str(get_locale()), title=title,
                           contacts=contacts, work_hours=work_hours)


@blueprint.route('/book/<id>', methods=['GET', 'POST'])
@logger.catch()
def show_arrival(id):
    book = NewBooks.query.filter_by(id=id).first()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    partners = Partners.query.all()
    full_nav = dict()
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()

    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    resp = make_response(
        render_template('public_bp/public_arrival.html', book=book, menu=full_nav, partners=partners,
                        fast_access=fast_access, locale=str(get_locale()), title=book, contacts=contacts,
                        work_hours=work_hours))
    resp.headers['Content-Type'] = 'text/html'
    return resp


@blueprint.route('/book_img/<id>')
@logger.catch()
def book_img(id):
    img = NewBooks.query.get(id).image
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h
