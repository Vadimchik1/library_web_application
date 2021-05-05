from flask import Blueprint

blueprint = Blueprint('error', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/errors/static/')

from app.errors import routes
