import os

class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') if os.environ.get('SECRET_KEY') else 'e133c32c00b2eb8f676e8695531d0ee3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') if os.environ.get('SQLALCHEMY_DATABASE_URI') else 'sqlite:///site.db'
    POST_PER_PAGE = 5
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME= os.environ.get('MAIL_UER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')