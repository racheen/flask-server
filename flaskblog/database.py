from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(DATABASE_URI,echo=False, connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(autocommit=False,autoflush=False,bind=engine)
session = DBSession()

def init_db():
    from models import User, Post
    Base.metadata.create_all(bind=engine)