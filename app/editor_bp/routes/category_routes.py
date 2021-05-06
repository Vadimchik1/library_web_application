from flask import render_template, current_app, redirect, url_for, flash, request
from app.editor_bp import blueprint
from ..forms import AddCategoryForm, AddRecordForm
from app.models import db, Category, Record


def get_category_id(name):
    cats = Category.query.all()
    for i in cats:
        if i.name == name:
            return i.id


# @blueprint.route('/add-category', methods=['GET', 'POST'])
# def add_category():
#     form = AddCategoryForm()
#     if form.validate_on_submit():
#         category = Category(name=form.name.data)
#         db.session.add(category)
#         db.session.commit()
#         return redirect(url_for('editor.add_category'))
#     return render_template('editor_bp/add_category.html', form=form)


@blueprint.route('/categories/', methods=['GET', 'POST'])
def show_categories():
    categories = Category.query.all()
    return render_template('editor_bp/categories.html', categories=categories)


@blueprint.route('/insert-category', methods=['POST'])
def insert_category():
    if request.method == 'POST':
        name = request.form['name']
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Категория была успешно добавлена')
        return redirect(url_for('editor.show_categories'))


@blueprint.route('/update-category', methods=['POST'])
def update_category():
    if request.method == 'POST':
        category = Category.query.get(request.form.get('id'))
        category.name = request.form['name']
        db.session.add(category)
        db.session.commit()
        flash("Employee was changed successfully")
        return redirect(url_for('editor.show_categories'))


@blueprint.route('/delete-category/<id>/', methods=['GET', 'POST'])
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    flash("Категория была успешно удалена")
    return redirect(url_for('editor.show_categories'))


@blueprint.route('/categories/<id>', methods=['GET', 'POST'])
def category(id):
    records = Record.query.filter_by(category_id=id).all()
    category_name = Category.query.filter_by(id=id).first().name
    return render_template('editor_bp/category.html', records=records, category_name=category_name)


@blueprint.route('record/<id>', methods=['GET', 'POST'])
def record(id):
    # edit_record | show_record in admin panel
    record_item = Record.query.filter_by(category_id=id).first()
    if request.method == 'POST':
        record_item.name = request.form['name']
        record_item.text = request.form['editordata']
        record_item.photo = None
        db.session.add(record_item)
        db.session.commit()
        return redirect(url_for('editor.category', id=record_item.category_id))
    return render_template('editor_bp/edit_record.html', record_item=record_item)


@blueprint.route('/add-record', methods=['GET', 'POST'])
def add_record():
    form = AddRecordForm()
    categories = Category.query.all()
    # if form.validate_on_submit():
    #     record = Record(name=form.name.data, text=form.text.data, category_id=int(form.category.data))
    #     db.session.add(record)
    #     db.session.commit()
    #     return redirect(url_for('editor.add_record'))
    if request.method == 'POST':
        print(request.form['category'])
        category_name = request.form['category']
        record = Record(name=request.form['name'], category_id=get_category_id(category_name), photo=None,
                        text=request.form['editordata'])
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('editor.add_record'))
    return render_template('editor_bp/add_record.html', form=form, categories=categories)


@blueprint.route('/delete-record/<id>/', methods=['GET', 'POST'])
def delete_record(id):
    record = Record.query.get(id)
    id_r = record.category_id
    db.session.delete(record)
    db.session.commit()
    flash("Запись была успешно удалена")
    return redirect(url_for('editor.category', id=id_r))
