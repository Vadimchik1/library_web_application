from flask import render_template, request, redirect, url_for
from app.editor_bp import blueprint
from app.models import Readers, db
from flask_user import roles_required
from loguru import logger


@blueprint.route('/readers')
@roles_required(['editor', 'admin'])
@logger.catch()
def readers():
    title = 'Читатели'
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    readers = Readers.query.order_by(Readers.id.desc())
    pages = readers.paginate(page=page, per_page=6)
    return render_template('editor_bp/readers.html', pages=pages, readers=readers, title=title)


@blueprint.route('/readers/<id>')
@roles_required(['editor', 'admin'])
@logger.catch()
def show_reader(id):
    title = 'Информация о читателе'
    reader = Readers.query.filter_by(id=id).first()
    return render_template('editor_bp/reader.html', title=title, reader=reader)


@blueprint.route('/readers/delete/<id>')
@roles_required(['editor', 'admin'])
@logger.catch()
def delete_reader(id):
    reader = Readers.query.filter_by(id=id).first()
    db.session.delete(reader)
    db.session.commit()
    return redirect(url_for('editor.readers'))
