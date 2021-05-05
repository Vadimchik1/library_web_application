from flask import Blueprint

blueprint = Blueprint('editor', __name__,
                      url_prefix='/edit',
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/editor_bp/static/')

from app.editor_bp.routes import core
