import os
from boto.s3.connection import S3Connection as conf

class Config:
    dev = False
    if dev == True:
        SECRET_KEY = os.environ['SECRET_KEY']
        DATABASE_URI= os.environ['DATABASE_URI']
        MAIL_SERVER = os.environ['MAIL_SERVER']
        MAIL_PORT = os.environ['MAIL_PORT']
        MAIL_USE_TLS = True
        MAIL_USE_SSL = False
        MAIL_USERNAME = os.environ['MAIL_USERNAME']
        MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    else:
        SECRET_KEY = conf(os.environ['SECRET_KEY'])
        DATABASE_URI= conf(os.environ['DATABASE_URI'])
        MAIL_SERVER = conf(os.environ['MAIL_SERVER'])
        MAIL_PORT = conf(os.environ['MAIL_PORT'])
        MAIL_USE_TLS = True
        MAIL_USE_SSL = False
        MAIL_USERNAME = conf(os.environ['MAIL_USERNAME'])
        MAIL_PASSWORD = conf(os.environ['MAIL_PASSWORD'])