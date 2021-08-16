from flask import Flask, session
from flask_user import UserManager
from app.admin_bp import blueprint as admin_bp
from app.public_bp import blueprint as public_bp
from app.editor_bp import blueprint as edit_bp
from app.errors import blueprint as errors_bp
from config import ProductionConfig, DevelopingConfig
from app.models import *
from app.extensions import migrate, babel
from loguru import logger
import logging


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


@babel.localeselector
def get_locale():
    try:
        lang = session['language']
    except KeyError:
        return 'ru'
    return lang


def create_usermanager(app, db, User):
    user_manager = UserManager(app, db, User)
    return user_manager


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)

    # user_manager = UserManager(app, db, User)
    user_manager = create_usermanager(app, db, User)

    logger.start(app.config['LOGFILE'], level=app.config['LOG_LEVEL'], format="{time} {level} {message}",
                 backtrace=app.config['LOG_BACKTRACE'], rotation='25 MB', serialize=True)

    # register loguru as handler
    app.logger.addHandler(InterceptHandler())
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(errors_bp)
    return app
