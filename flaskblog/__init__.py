import os
from flask import Flask
from config import SECRET_KEY, MAIL_PASS, MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USER, MAIL_USE_TLS, DATABASE_URI
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.database import init_db
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DATABASE_URI'] = DATABASE_URI

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USER
app.config['MAIL_PASSWORD'] = MAIL_PASS
mail = Mail(app)


init_db()

from flaskblog import routes