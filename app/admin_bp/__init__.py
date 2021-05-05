# -*- coding: utf-8 -*-
from flask import Blueprint

blueprint = Blueprint('admin', __name__,
                      url_prefix='/admin',
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/admin/static/')

from app.admin_bp.routes.core import *