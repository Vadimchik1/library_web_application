from flask import render_template, request, redirect, url_for, flash
from flask.debughelpers import DebugFilesKeyError
from app.editor_bp import blueprint
from app.models import NewBooks, db
from flask_user import roles_required
from pathlib import Path
from .partners import files_suffixes

from loguru import logger


@blueprint.route('/new_arrivals')
@roles_required(['editor', 'admin'])
# @logger.catch()
def new_arrivals():
    title = 'Новые поступления'
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    books = NewBooks.query.order_by(NewBooks.id.desc())
    pages = books.paginate(page=page, per_page=6)
    return render_template('editor_bp/new_arrivals.html', pages=pages, books=books, title=title)


@blueprint.route('/add_new_arrival', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
# @logger.catch()
def add_new_arrival():
    title = 'Добавить книгу'
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if Path(request.files['file'].filename).suffix not in files_suffixes:
            flash('Расширение файла не "jpg" или не был отправлен файл.')
            return redirect(url_for('editor.add_record'))
        image = request.files['file'].read()
        text = request.form['editordata']
        new_book = NewBooks(title=name, description=description, image=image, text=text)
        db.session.add(new_book)
        db.session.commit()
        flash('Книга была успешно добавлена')
        return redirect(url_for('editor.add_new_arrival'))
    return render_template('editor_bp/add_new_arrival.html', title=title)


@blueprint.route('/change_arrival/<id>', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
# @logger.catch()
def change_arrival(id):
    title = 'Изменить информацию о книге'
    book = NewBooks.query.filter_by(id=id).first()
    if request.method == 'POST':
        book.name = request.form['name']
        book.name_en = request.form['name_en']
        book.name_kz = request.form['name_kz']
        book.description = request.form['description']
        book.description_en = request.form['description_en']
        book.description_kz = request.form['description_kz']
        book.text = request.form['editordata']
        book.text_en = request.form['editordata_en']
        book.text_kz = request.form['editordata_kz']
        try:
            image = request.files['file'].read()
            if str(image) == "b''":
                pass
            else:
                if Path(request.files['file'].filename).suffix not in files_suffixes:
                    flash('Расширение файла не "jpg"')
                    return redirect(url_for('editor.change_arrival', id=id))
                book.image = image
        except DebugFilesKeyError:
            pass
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('editor.new_arrivals'))
    return render_template('editor_bp/change_arrival.html', title=title, book=book)


@blueprint.route('/change_arrival', methods=['POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def delete_arrival():
    book = NewBooks.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    flash('Книга была успешно удалена')
    return redirect(url_for('editor.new_arrivals'))
