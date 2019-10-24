from flask import render_template, request, Blueprint
from sqlalchemy_paginator import Paginator
from flaskblog.database import session
from flaskblog.models import Post
from flaskblog.users.utils import pagination

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    query = session.query(Post).order_by(Post.date_posted.desc())
    posts = Paginator(query, 5)
    if page > posts.pages_range[-1]:
        return render_template("errors/404.html")
    posts_page = posts.page(page)
    show_pages = pagination(page, posts.pages_range)
    return render_template('home.html', posts_page=posts_page, posts=posts, show_pages=show_pages)

@main.route("/about")
def about():
    return render_template('about.html', title='About')