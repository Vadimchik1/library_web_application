from flask import redirect, url_for
from app.editor_bp import blueprint
from flask_user import roles_required
from loguru import logger


@blueprint.route('/')
@blueprint.route('/index')
@roles_required(['editor', 'admin'])
@logger.catch()
def index():
    return redirect(url_for('editor.add_record'))




