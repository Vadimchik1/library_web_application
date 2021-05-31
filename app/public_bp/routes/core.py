from flask import render_template, make_response, url_for, request, session, redirect
from app.public_bp import blueprint
from app.models import Record, Menu, db, SubMenu, Partners, FastAccess


@blueprint.route('/')
@blueprint.route('/index')
def index():
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
    return render_template('public_bp/public_category.html', records=records, menu=full_nav, partners=partners,
                           fast_access=fast_access, pages=pages)


@blueprint.route('/categories/<id>', methods=['GET', 'POST'])
def category(id):
    records = Record.query.filter_by(category_id=id).order_by(Record.created_at.desc())
    partners = Partners.query.all()

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
                           fast_access=fast_access, pages=pages, categ_id=id)


@blueprint.route('/record/<id>', methods=['GET', 'POST'])
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
                        fast_access=fast_access))
    resp.headers['Content-Type'] = 'text/html'
    return resp


@blueprint.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('public.index'))

@blueprint.route('/partner_img/<id>')
def partner_img(id):
    img = Partners.query.get(id).image
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@blueprint.route('/record_img/<id>')
def record_img(id):
    img = Record.query.get(id).photo
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

# @blueprint.route('/')
# @blueprint.route('/index')
# def index():
#     records = Record.query.all()
#     partners = Partners.query.all()
#     fast_access = FastAccess.query.order_by(FastAccess.index).all()
#     menu = db.session.query(Menu).order_by(Menu.index).all()
#
#     full_nav = dict()
#     for el in menu:
#         list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
#         full_nav[el] = list_submenu
#     return render_template('public_bp/public_category.html', records=records, menu=full_nav, partners=partners,
#                            fast_access=fast_access)

# @blueprint.route('/categories/<id>', methods=['GET', 'POST'])
# def category(id):
#     records = Record.query.filter_by(category_id=id).all()
#     partners = Partners.query.all()
#     # category_name = Category.query.filter_by(id=id).first().name
#     menu = db.session.query(Menu).order_by(Menu.index).all()
#     fast_access = FastAccess.query.order_by(FastAccess.index).all()
#     full_nav = dict()
#     for el in menu:
#         list_submenu = db.session.query(SubMenu).filter_by(menu_parent_id=el.id).order_by(SubMenu.index).all()
#         full_nav[el] = list_submenu
#     return render_template('public_bp/public_category.html', records=records, menu=full_nav, partners=partners,
#                            fast_access=fast_access)
