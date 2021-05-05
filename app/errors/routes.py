# -*- coding: utf-8 -*-
from flask import render_template
# from flask_babel import lazy_gettext as _l
from app.errors import blueprint


@blueprint.app_errorhandler(403)
def not_found_error(error):
    return render_template('error.html', content='Извините, доступ запрещен!'), 403


@blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', content='Извините, страница не найдена!'), 404


@blueprint.app_errorhandler(500)
def internal_error(error):
    return render_template('error.html', content='Извините, Что-то пошло не так.'), 500
