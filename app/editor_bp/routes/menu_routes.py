from flask import render_template, request, redirect, url_for, flash, jsonify
from app.editor_bp import blueprint
from app.models import Menu, db, SubMenu


def get_inner_url(url):
    if len(url.split('/')) == 3:
        return url
    result = '/'.join(url.split('/')[3:])
    return result


@blueprint.route('/menu/')
def menu():
    title = 'Меню'
    menu_list = Menu.query.all()

    return render_template('editor_bp/menu.html', menu_list=menu_list, title=title)


@blueprint.route('/insert_menu_parent', methods=['POST'])
def insert_menu_parent():
    if request.method == 'POST':
        name = request.form['name']
        index_el = len(Menu.query.all()) + 1
        is_parent = True
        menu_el = Menu(name=name, is_parent=is_parent, url_is_inner=None, url=None, index=index_el)
        db.session.add(menu_el)
        db.session.commit()
        flash('Категория была успешно добавлена')
        return redirect(url_for('editor.menu'))


@blueprint.route('/insert_menu_link', methods=['POST'])
def insert_menu_link():
    if request.method == 'POST':
        name = request.form['name']
        index_el = len(Menu.query.all()) + 1
        if 'inner' in request.form:
            is_inner = True
        else:
            is_inner = False
        if is_inner:
            url = get_inner_url(request.form['url'])
        else:
            url = request.form['url']
        print(request.form['url'])
        print('it is url: ', url, '')
        menu_el = Menu(name=name, is_parent=False, url_is_inner=is_inner, url=url, index=index_el)
        db.session.add(menu_el)
        db.session.commit()
        flash('Категория была успешно добавлена')
        return redirect(url_for('editor.menu'))


@blueprint.route('/update-menu_parent', methods=['POST'])
def update_menu_parent():
    if request.method == 'POST':
        menu_el = Menu.query.get(request.form.get('id'))
        menu_el.name = request.form['name']
        if menu_el.is_parent == False:
            menu_el.url = request.form['url']
        db.session.add(menu_el)
        db.session.commit()
        flash("Название было изменено")
        return redirect(url_for('editor.menu'))


@blueprint.route('/delete_menu_parent/<id>', methods=['GET', 'POST'])
def delete_menu_parent(id):
    menu_el = Menu.query.get(id)
    index_del_el = menu_el.index
    submenu = SubMenu.query.filter_by(menu_parent_id=id).all()
    for i in submenu:
        db.session.delete(i)
    db.session.delete(menu_el)
    db.session.commit()
    menu_els = Menu.query.all()
    for el in menu_els:
        if el.index > index_del_el:
            el.index -= 1
            db.session.add(el)
    db.session.commit()

    flash("Элемент был успешно удален")
    return redirect(url_for('editor.menu'))


@blueprint.route('/menu/change-location/')
def drag_drop_menu():
    # dragdrop = Menu.query.all()
    drag_drop = db.session.query(Menu).order_by(Menu.index).all()
    print(drag_drop)
    return render_template('editor_bp/drag_drop_menu.html', dragdrop=drag_drop, title='Изменение меню')


@blueprint.route('/menu/change-location/updateList', methods=["POST"])
def update_menu_location():
    if request.method == 'POST':
        order = request.form['order'].split(',')
        count = 0
        for value in order:
            count += 1
            el = Menu.query.filter_by(id=value).first()
            el.index = count
            db.session.add(el)
            db.session.commit()
        return jsonify('Порядок был изменен')


@blueprint.route('/submenu/change-location/updateList', methods=["POST"])
def update_submenu_location():
    if request.method == 'POST':
        order = request.form['order'].split(',')
        count = 0
        for value in order:
            count += 1
            el = SubMenu.query.filter_by(id=value).first()
            el.index = count
            db.session.add(el)
            db.session.commit()
        return jsonify('Порядок был изменен')


@blueprint.route('/show_menu_element/<id>', methods=['GET', 'POST'])
def show_menu_element(id):
    menu_el_children = SubMenu.query.filter_by(menu_parent_id=id).all()
    menu_name = Menu.query.filter_by(id=id).first().name
    return render_template('editor_bp/menu_element.html', menu_el_children=menu_el_children, menu_name=menu_name,
                           parent_id=id, title=menu_name)


@blueprint.route('/insert_submenu/<id>', methods=['POST'])
def insert_submenu(id):
    if request.method == 'POST':
        name = request.form['name']
        index_el = len(SubMenu.query.filter_by(menu_parent_id=id).all()) + 1
        if 'inner' in request.form:
            is_inner = True
        else:
            is_inner = False

        if is_inner:
            url = get_inner_url(request.form['url'])
        else:
            url = request.form['url']
        menu_el = SubMenu(name=name, url_is_inner=is_inner, url=url, menu_parent_id=id, index=index_el)
        db.session.add(menu_el)
        db.session.commit()
        flash('Категория была успешно добавлена')
        return redirect(url_for('editor.show_menu_element', id=menu_el.menu_parent_id))


# Надо писать здесь создание вставка подменю элемента

@blueprint.route('/update_submenu/', methods=['POST'])
def update_submenu():
    if request.method == 'POST':
        print(request)
        submenu_el = SubMenu.query.get(request.form.get('id'))
        submenu_el.name = request.form['name']
        submenu_el.url = request.form['url']
        db.session.add(submenu_el)
        db.session.commit()
        flash("Название было изменено")
        return redirect(url_for('editor.show_menu_element', id=submenu_el.menu_parent_id))


@blueprint.route('/delete_submenu/<id>', methods=['GET', 'POST'])
def delete_submenu(id):
    submenu_el = SubMenu.query.get(id)
    index_del_el = submenu_el.index
    parent_id = submenu_el.menu_parent_id
    db.session.delete(submenu_el)
    db.session.commit()
    submenu_els = SubMenu.query.filter_by(menu_parent_id=parent_id).all()
    for el in submenu_els:
        if el.index > index_del_el:
            el.index -= 1
            db.session.add(el)
    db.session.commit()
    flash("Элемент был успешно удален")
    return redirect(url_for('editor.show_menu_element', id=parent_id))
