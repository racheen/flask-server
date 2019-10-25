import os

class Config:
    # SECRET_KEY="u'a124ad2c6e71c86be14421df74761051"
    # DATABASE_URI='postgres://postgres:admin@localhost:5432/flask-server38'
    # MAIL_SERVER = 'smtp.mailtrap.io'
    # MAIL_PORT = 2525
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = '3f118538243430'
    # MAIL_PASSWORD = 'c9c4b0be481af8'
    SECRET_KEY= os.environ['SECRET_KEY']
    DATABASE_URI= os.environ['DATABASE_URI']
    MAIL_SERVER = os.environ['MAIL_SERVER']'
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']