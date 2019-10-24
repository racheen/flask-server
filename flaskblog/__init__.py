from flask import Flask
# from config import SECRET_KEY, MAIL_PASS, MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USER, MAIL_USE_TLS, DATABASE_URI
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.database import init_db
from flask_mail import Mail
from flaskblog.config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
init_db()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
