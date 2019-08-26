from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Base, Post

engine = create_engine('sqlite:///site2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user_1 = User(username = 'Corey', email='C@email.com', password='password')
user_2 = User(username = 'John Doe', email='jd@email.com', password='password')
session.add(user_1)
session.add(user_2)
session.commit()

print session.query(User).all()
print "added users!"