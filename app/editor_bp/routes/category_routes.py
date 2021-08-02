from flask import render_template, redirect, url_for, flash, request
from app.editor_bp import blueprint
from flask.debughelpers import DebugFilesKeyError
from ..forms import AddRecordForm
from app.models import db, Category, Record
from datetime import datetime
from pathlib import Path
from .partners import files_suffixes
from flask_user import roles_required
from loguru import logger


def get_category_id(name):
    cats = Category.query.all()
    for i in cats:
        if i.name == name:
            return i.id


def valid_record_data(req):
    if req.form['name'] == '':
        flash('Поле название было оставлено пустым')
        return redirect(url_for('editor.add_record'))
    elif req.form['description'] == '':
        flash('Поле с описанием было оставлено пустым')
        return redirect(url_for('editor.add_record'))
    elif req.form['editordata'] == '':
        flash('Поле с наполнением было оставлено пустым')
        return redirect(url_for('editor.add_record'))




@blueprint.route('/categories/', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def show_categories():
    title = 'Категории'
    categories = Category.query.all()
    return render_template('editor_bp/categories.html', categories=categories, title=title)


@blueprint.route('/insert-category', methods=['POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def insert_category():
    if request.method == 'POST':
        name = request.form['name']
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        cat = Category.query.filter_by(name=request.form['name']).first()
        cat.url = f'/categories/{cat.id}'
        db.session.add(cat)
        db.session.commit()
        flash('Категория была успешно добавлена')
        return redirect(url_for('editor.show_categories'))


@blueprint.route('/update-category', methods=['POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def update_category():
    if request.method == 'POST':
        category = Category.query.get(request.form.get('id'))
        category.name = request.form['name']
        db.session.add(category)
        db.session.commit()
        flash("Employee was changed successfully")
        return redirect(url_for('editor.show_categories'))


@blueprint.route('/delete-category/<id>', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()
    flash("Категория была успешно удалена")
    return redirect(url_for('editor.show_categories'))


@blueprint.route('/categories/<id>', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def category(id):
    records = Record.query.filter_by(category_id=id).all()
    category_name = Category.query.filter_by(id=id).first().name
    title = category_name
    return render_template('editor_bp/category.html', records=records, category_name=category_name, title=title)


@blueprint.route('record/<id>', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def record(id):
    # edit_record | show_record in admin panel
    record_item = Record.query.filter_by(id=id).first()
    if record_item is None:
        flash('Вы ввели несуществующий id.')
        return redirect(url_for('editor.find_edit_record'))
    try:
        title = record_item.name
    except:
        title = ''
    if request.method == 'POST':
        record_item.name = request.form['name']
        record_item.name_en = request.form['name_en']
        record_item.name_kz = request.form['name_kz']
        record_item.description = request.form['description']
        record_item.description_en = request.form['description_en']
        record_item.description_kz = request.form['description_kz']

        record_item.text = request.form['editordata']
        record_item.text_en = request.form['editordata_en']
        record_item.text_kz = request.form['editordata_kz']

        try:
            image = request.files['file'].read()
            if str(image) == "b''":
                pass
            else:
                if Path(request.files['file'].filename).suffix not in files_suffixes:
                    flash('Расширение файла не "jpg"')
                    return redirect(url_for('editor.change_arrival', id=id))
                record_item.image = image
        except DebugFilesKeyError:
            pass
        record_item.created_at = datetime.utcnow()
        db.session.add(record_item)
        db.session.commit()
        return redirect(url_for('editor.category', id=record_item.category_id))
    return render_template('editor_bp/edit_record.html', record_item=record_item, title=title)


@blueprint.route('/add-record', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def add_record():
    form = AddRecordForm()
    categories = Category.query.all()
    title = 'Новая запись'
    if request.method == 'POST':
        description = (request.form['description'])
        category_name = request.form['category']
        exist_names = []
        for record in Record.query.all():
            exist_names.append(record.name)
        if request.form['name'] in exist_names:
            flash('Такое название уже существует, пожалуйста введите другое!')
            return redirect(url_for('editor.add_record'))
        valid_record_data(request)
        if Path(request.files['file'].filename).suffix not in files_suffixes:
            flash('Расширение файла не "jpg" или не был отправлен файл.')
            return redirect(url_for('editor.add_record'))
        image = request.files['file'].read()
        record = Record(name=request.form['name'], category_id=get_category_id(category_name), photo=image,
                        text=request.form['editordata'], description=description)
        db.session.add(record)
        db.session.commit()
        rec = Record.query.filter_by(name=request.form['name']).first()
        rec.url = f'/record/{rec.id}'
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('editor.add_record'))
    return render_template('editor_bp/add_record.html', form=form, categories=categories, title=title)


@blueprint.route('/delete-record/<id>/', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def delete_record(id):
    record = Record.query.get(id)
    id_r = record.category_id
    db.session.delete(record)
    db.session.commit()
    flash("Запись была успешно удалена")
    return redirect(url_for('editor.category', id=id_r))


@blueprint.route('/find-edit-record/', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def find_edit_record():
    title = 'Поиск записи'
    if request.method == 'POST':
        data = request.form['record_id']
        if data.isdigit() == False:
            flash('Пожалуйста введите в это поле цифру!')
            return redirect(url_for('editor.find_edit_record'))
        return redirect(url_for('editor.record', id=int(request.form['record_id'])))
    return render_template('editor_bp/find_edit_record.html', title=title)
