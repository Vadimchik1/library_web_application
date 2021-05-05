from flask import render_template, request, redirect, url_for
from app.editor_bp import blueprint
from app.models import Menu


@blueprint.route('/menu/')
def menu():
    return render_template('editor_bp/menu.html')


@blueprint.route('/insert-category', methods=['POST'])
def insert_menu_parent():
    if request.method == 'POST':
        name = request.form['name']

        menu_el = Menu(name=name)
        # db.session.add(category)
        # db.session.commit()
        # flash('Категория была успешно добавлена')
        return redirect(url_for('editor.show_categories'))
