from flask import render_template, request, redirect, url_for, flash, jsonify
from app.editor_bp import blueprint
from .menu_routes import get_inner_url
from app.models import FastAccess, db
from flask_user import roles_required
from loguru import logger


@blueprint.route('/fast_access/')
@roles_required(['editor', 'admin'])
@logger.catch()
def fast_access():
    title = 'Быстрый доступ'
    menu_list = FastAccess.query.all()

    return render_template('editor_bp/fast_access.html', menu_list=menu_list, title=title)


@blueprint.route('/insert_fast_access', methods=['POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def insert_fast_access():
    if request.method == 'POST':
        name = request.form['name']
        index_el = len(FastAccess.query.all()) + 1
        if 'inner' in request.form:
            is_inner = True
        else:
            is_inner = False
        if is_inner:
            url = '/' + get_inner_url(request.form['url'])

        else:
            url = request.form['url']
        fast_access_el = FastAccess(name=name, url_is_inner=is_inner, url=url, index=index_el)
        db.session.add(fast_access_el)
        db.session.commit()
        flash('Элемент навигационной панели был успешно добавлен')
        return redirect(url_for('editor.fast_access'))


@blueprint.route('/update_fast_access/', methods=['POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def update_fast_access():
    if request.method == 'POST':
        fast_access_el = FastAccess.query.get(request.form.get('id'))
        fast_access_el.name = request.form['name']
        fast_access_el.name_en = request.form['name_en']
        fast_access_el.name_kz = request.form['name_kz']
        fast_access_el.url = request.form['url']
        db.session.add(fast_access_el)
        db.session.commit()
        flash("Нафигационный элемент был изменен")
        return redirect(url_for('editor.fast_access'))


@blueprint.route('/delete_fast_access/<id>', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def delete_fast_access(id):
    fast_access_el = FastAccess.query.get(id)
    index_del_el = fast_access_el.index
    db.session.delete(fast_access_el)
    db.session.commit()
    fast_access_els = FastAccess.query.all()
    for el in fast_access_els:
        if el.index > index_del_el:
            el.index -= 1
            db.session.add(el)
    db.session.commit()
    flash("Элемент был успешно удален")
    return redirect(url_for('editor.fast_access'))


@blueprint.route('/fast_access/change-location/')
@roles_required(['editor', 'admin'])
@logger.catch()
def drag_drop_fast_access():
    drag_drop = db.session.query(FastAccess).order_by(FastAccess.index).all()
    return render_template('editor_bp/drag_drop_fast_access.html', dragdrop=drag_drop, title='Изменение навигации')


@blueprint.route('/fast_access/change-location/updateList', methods=["POST"])
@roles_required(['editor', 'admin'])
@logger.catch()
def update_fast_access_location():
    if request.method == 'POST':
        order = request.form['order'].split(',')
        count = 0
        for value in order:
            count += 1
            el = FastAccess.query.filter_by(id=value).first()
            el.index = count
            db.session.add(el)
            db.session.commit()
        return jsonify('Порядок был изменен')
