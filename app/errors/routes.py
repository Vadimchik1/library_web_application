# -*- coding: utf-8 -*-
from flask import render_template
from app.errors import blueprint
from loguru import logger


@blueprint.app_errorhandler(403)
@logger.catch()
def not_found_error(error):
    return render_template('error.html', content='Извините, доступ запрещен!'), 403


@blueprint.app_errorhandler(404)
@logger.catch()
def not_found_error(error):
    return render_template('error.html', content='Извините, страница не найдена!'), 404


@blueprint.app_errorhandler(500)
@logger.catch()
def internal_error(error):
    return render_template('error.html', content='Извините, Что-то пошло не так.'), 500
