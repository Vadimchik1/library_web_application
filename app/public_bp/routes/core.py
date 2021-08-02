from flask import render_template, make_response, url_for, request, session, redirect, flash
from app.public_bp import blueprint
from app.models import Record, Menu, db, SubMenu, Partners, FastAccess, Category, Questions, Readers, NewBooks, Contacts, WorkHours
from flask_babel import get_locale, _
import datetime
from loguru import logger


def normalize_date(html_date: str):
    date: list = html_date.split('-')
    date_list = [int(item) for item in date]
    python_date = datetime.date(date_list[0], date_list[1], date_list[2])
    return python_date


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


@blueprint.route('/categories/<id>', methods=['GET', 'POST'])
@logger.catch()
def category(id):
    records = Record.query.filter_by(category_id=id).order_by(Record.created_at.desc())
    partners = Partners.query.all()

    categ_title = Category.query.filter_by(id=id).first()

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = records.paginate(page=page, per_page=4)
    menu = db.session.query(Menu).order_by(Menu.index).all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    contacts = Contacts.query.first()
    work_hours = WorkHours.query.first()

    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    return render_template('public_bp/public_category_show.html', records=records, menu=full_nav, partners=partners,
                           fast_access=fast_access, pages=pages, categ_id=id, locale=str(get_locale()),
                           title=categ_title, contacts=contacts, work_hours=work_hours)


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
                        fast_access=fast_access, locale=str(get_locale()), title=record, contacts=contacts, work_hours=work_hours))
    resp.headers['Content-Type'] = 'text/html'
    return resp


@blueprint.route('/partner_img/<id>')
@logger.catch()
def partner_img(id):
    img = Partners.query.get(id).image
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@blueprint.route('/record_img/<id>')
@logger.catch()
def record_img(id):
    img = Record.query.get(id).photo
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@blueprint.route('/book_img/<id>')
@logger.catch()
def book_img(id):
    img = NewBooks.query.get(id).image
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


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


@blueprint.route('/language/<language>')
@logger.catch()
def set_language(language=None, url=None):
    session['language'] = language
    return redirect(url_for('public.index'))


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


@blueprint.route('/enroll', methods=['GET', 'POST'])
# @logger.catch()
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


@blueprint.route('/new_arrivals')
# @logger.catch()
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
# @logger.catch()
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
                        fast_access=fast_access, locale=str(get_locale()), title=book, contacts=contacts, work_hours=work_hours))
    resp.headers['Content-Type'] = 'text/html'
    return resp
