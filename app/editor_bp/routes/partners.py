from flask import render_template, request, redirect, url_for, flash, jsonify
from pathlib import Path
from app.editor_bp import blueprint
from app.models import Partners, db
from PIL import Image

files_suffixes = ['.jpg', '.png']
@blueprint.route('/partners')
def show_partners():
    partners = Partners.query.all()
    print(partners)
    return render_template('editor_bp/partners.html', partners=partners, title='Партнеры')


@blueprint.route('/add_partner', methods=['GET', 'POST'])
def add_partner():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url_address']
        if name == '':
            flash('Не было введено название файла...')
            return redirect(url_for('editor.add_partner'))
        if url == '':
            flash('Не был введен адрес ссылки...')
            return redirect(url_for('editor.add_partner'))
        if Path(request.files['file'].filename).suffix not in files_suffixes:
            flash('Расширение файла не "jpg" или не был отправлен файл.')
            return redirect(url_for('editor.add_partner'))

        image = request.files['file'].read()

        partner = Partners(name=name, url=url, image=image)
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('editor.show_partners'))
    return render_template('editor_bp/add_partner.html', title='Добавить партнера')

@blueprint.route('/delete_partner/<id>', methods=['GET', 'POST'])
def delete_partner(id):
    partner = Partners.query.get(id)
    db.session.delete(partner)
    db.session.commit()
    flash("Партнер был успешно удален...")
    return redirect(url_for('editor.show_partners'))