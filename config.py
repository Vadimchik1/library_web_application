class Config:
    DEBUG = True
    LANGUAGES = ['en', 'ru', 'kz']
    SECRET_KEY = 'supersecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bible.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRSF_ENABLED = True
    USER_APP_NAME = 'Flask-User Application'
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
