from flask import render_template
from app.editor_bp import blueprint
from flask_user import roles_required
from loguru import logger


@blueprint.route('/')
@blueprint.route('/index')
@roles_required(['editor', 'admin'])
@logger.catch()
def index():
    return render_template('editor_bp/index.html')




