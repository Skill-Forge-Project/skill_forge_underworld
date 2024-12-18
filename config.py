import os
from app.database_conn import SQL_URI

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = SQL_URI
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_DOMAIN = False
    TIMEZONE = 'Europe/Sofia'
    PREFERRED_URL_SCHEME = 'https'