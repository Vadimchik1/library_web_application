# -*- coding: utf-8 -*-
from flask import Blueprint

blueprint = Blueprint('public', __name__,
                      url_prefix='',
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/admin/static/')

from app.public_bp.routes import core