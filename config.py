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

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Ensure cookies are sent over HTTPS
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False  # Ensure remember me cookie is sent over HTTPS