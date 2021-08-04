from flask import render_template, request, redirect, url_for
from app.editor_bp import blueprint
from app.models import Questions, db
from flask_user import roles_required
from loguru import logger


@blueprint.route('/questions')
@roles_required(['editor', 'admin'])
@logger.catch()
def questions():
    title = 'Виртуальная справочная служба'
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    questions = Questions.query.order_by(Questions.id.desc())
    pages = questions.paginate(page=page, per_page=6)
    return render_template('editor_bp/questions.html', pages=pages, questions=questions, title=title)


@blueprint.route('/questions/<id>')
@roles_required(['editor', 'admin'])
@logger.catch()
def show_question(id):
    title = 'Виртуальная справочная служба'
    question = Questions.query.filter_by(id=id).first()
    return render_template('editor_bp/question.html', title=title, question=question)


@blueprint.route('/questions/delete/<id>')
@roles_required(['editor', 'admin'])
@logger.catch()
def delete_question(id):
    reader = Questions.query.filter_by(id=id).first()
    db.session.delete(reader)
    db.session.commit()
    return redirect(url_for('editor.questions'))
