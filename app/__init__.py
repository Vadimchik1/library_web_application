from flask import Flask, request, session, current_app
from flask_user import SQLAlchemyAdapter, UserManager
from app.admin_bp import blueprint as admin_bp
from app.public_bp import blueprint as public_bp
from app.editor_bp import blueprint as edit_bp
from app.errors import blueprint as errors_bp
from config import Config
from app.models import *
from app.extensions import migrate, babel
from flask_script import Manager


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    elif not session.get('lang'):
        session['lang'] = request.accept_languages.best_match(current_app.config['LANGUAGES'])

    return session.get('lang', 'ru')


def create_usermanager(app, db, User):
    user_manager = UserManager(app, db, User)
    return user_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)

    # user_manager = UserManager(app, db, User)
    user_manager = create_usermanager(app, db, User)

    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(errors_bp)
    return app
