from flask import Flask
from config import SECRET_KEY
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.database import init_db

app = Flask(__name__)
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
init_db()

from flaskblog import routes