from flask import render_template, request
from app.models import db, Record, Partners, Category, Menu, FastAccess, Contacts, WorkHours, SubMenu
from app.public_bp import blueprint
from flask_babel import get_locale
from loguru import logger


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