from flask import Flask
from models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///flaskblog/site.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app.config['SECRET_KEY']="u'a124ad2c6e71c86be14421df74761051"

from flaskblog import routes