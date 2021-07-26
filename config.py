class Config:
    DEBUG = True
    LANGUAGES = ['en', 'ru', 'es']
    SECRET_KEY = 'supersecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bible.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRSF_ENABLED = True
    USER_APP_NAME = 'Сайт библиотеки'
    # USER_LOGIN_TEMPLATE = 'login.html'
    USER_ENABLE_REGISTER = False
    USER_ENABLE_CHANGE_PASSWORD = True  # чтобы поменять пароль авторизованный пользователь должен зайти на user/change_password

    # flask-mail
    USER_ENABLE_EMAIL = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USERNAME = 'vadimganica@gmail.com'
    MAIL_PASSWORD = '2559281335gh'
    MAIL_DEFAULT_SENDER = 'vadimganica@gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    POSTS_PER_PAGE = 10

    # set logging with loguru
    LOGFILE = "log.json"


class ProductionConfig(Config):
    DEBUG = False
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'


class DevelopingConfig(Config):
    DEBUG = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'INFO'
