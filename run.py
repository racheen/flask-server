from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)
    
# app.config['SECRET_KEY']="u'a124ad2c6e71c86be14421df74761051"
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

# db = SQLAlchemy(app)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return "Post('{}', '{}')".format(self.title, self.date_posted)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

#     def __repr__(self):
#         return "User('{}', '{}', '{}')".format(self.username,self.email,self.image_file)