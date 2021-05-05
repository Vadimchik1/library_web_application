from flask import render_template
from app.public_bp import blueprint


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return 'jopa'


