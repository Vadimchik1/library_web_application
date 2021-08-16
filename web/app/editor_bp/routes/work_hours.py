from flask import render_template, redirect, url_for, flash, request
from app.editor_bp import blueprint
from app.models import db, WorkHours

from flask_user import roles_required
from loguru import logger


@blueprint.route('/work_hours/', methods=['GET', 'POST'])
@roles_required(['editor', 'admin'])
@logger.catch()
def work_hours():
    title = 'Изменение часов работы. '
    work_hours = WorkHours.query.first()
    if request.method == 'POST':
        work_hours.text = request.form['text']
        work_hours.text_en = request.form['text_en']
        work_hours.text_kz = request.form['text_kz']
        db.session.add(work_hours)
        db.session.commit()
        flash('Часы работы успешно изменены')
        return redirect(url_for('editor.work_hours'))
    return render_template('editor_bp/work_hours.html', work_hours=work_hours, title=title)


