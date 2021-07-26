from flask import render_template, make_response, url_for, request, session, redirect, current_app, g
from app.public_bp import blueprint
from app.models import Record, Menu, db, SubMenu, Partners, FastAccess, Category, Questions
from flask_babel import get_locale, _
from loguru import logger


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
    for i in full_nav:
        print(i.name_en)
    return render_template('public_bp/public_category.html', records=records, menu=full_nav, partners=partners,
                           fast_access=fast_access, pages=pages, locale=str(get_locale()), title=title)


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
    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    print(id)
    return render_template('public_bp/public_category_show.html', records=records, menu=full_nav, partners=partners,
                           fast_access=fast_access, pages=pages, categ_id=id, locale=str(get_locale()),
                           title=categ_title)


@blueprint.route('/record/<id>', methods=['GET', 'POST'])
@logger.catch()
def show_record(id):
    record = Record.query.filter_by(id=id).first()
    menu = db.session.query(Menu).order_by(Menu.index).all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    partners = Partners.query.all()
    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    resp = make_response(
        render_template('public_bp/public_record.html', record=record, menu=full_nav, partners=partners,
                        fast_access=fast_access, locale=str(get_locale()), title=record))
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


@blueprint.route('/search')
@logger.catch()
def search():
    q = request.args.get('q')
    if q:
        records = Record.query.filter(
            Record.name.contains(q) | Record.description.contains(q) | Record.text.contains(q)).all()
        print(type(records))
        print(records)
    else:
        return redirect(url_for('public.index'))

    partners = Partners.query.all()
    fast_access = FastAccess.query.order_by(FastAccess.index).all()
    menu = db.session.query(Menu).order_by(Menu.index).all()

    full_nav = dict()
    for el in menu:
        list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
        full_nav[el] = list_submenu
    return render_template('public_bp/search.html', records=records, records_amount=len(records), menu=full_nav,
                           partners=partners,
                           fast_access=fast_access, locale=str(get_locale()))


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
    themes = ['Систематизация статей (УДК, МРНТИ', 'Электронная доставка статей',
              '	Систематизация учебно – методических пособий (УДК, ББК)',
              'Электронная доставка документов (15% от выбранного издания)',
              'Удаленный доступ к зарубежным информационным ресурсам']
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
        return redirect(url_for('public.contact_us'))
    return render_template('public_bp/contact_us.html', title=title, menu=full_nav, partners=partners,
                           fast_access=fast_access, themes=themes,
                           locale=str(get_locale()))
