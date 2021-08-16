import os

from dotenv import load_dotenv

load_dotenv()

DEV_DB = 'sqlite:///bible.db'

pg_user = str(os.getenv("pg_user"))
pg_pass = str(os.getenv("pg_pass"))
pg_db = str(os.getenv("pg_db"))
pg_host = 'db'
pg_port = 5432

PROD_DB = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'


class Config:
    DEBUG = True
    LANGUAGES = ['en', 'ru', 'es']
    SECRET_KEY = str(os.getenv("SECRET_KEY"))
    SQLALCHEMY_DATABASE_URI = DEV_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CRSF_ENABLED = True
    USER_APP_NAME = 'Сайт библиотеки'
    USER_ENABLE_REGISTER = False
    USER_ENABLE_CHANGE_PASSWORD = True  # чтобы поменять пароль авторизованный пользователь должен зайти на user/change_password

    # flask-mail
    USER_ENABLE_EMAIL = False
    POSTS_PER_PAGE = 10

    # set logging with loguru
    LOGFILE = "log.json"

    # flask babel
    BABEL_DEFAULT_LOCALE = 'ru'



class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB
    DEBUG = False
    LOG_BACKTRACE = False
    LOG_LEVEL = 'INFO'


class DevelopingConfig(Config):
    DEBUG = True
    LOG_BACKTRACE = True
    LOG_LEVEL = 'INFO'
