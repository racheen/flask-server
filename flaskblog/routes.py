import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy_paginator import Paginator
from flaskblog import app, bcrypt, login_manager, mail
from flaskblog.database import session
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

posts = []

def pagination(page, pages_range):
    show_pages = []
    if len(pages_range)<5:
        return pages_range
    if page + 2 >= pages_range[-1]:
        n = pages_range[-1] - 4
        while n!=pages_range[-1]+1:
            show_pages.append(n)
            n+=1
    elif page - 2 <= 1:
        n = 1
        while n!=6:
            show_pages.append(n)
            n+=1
    else:
        n = page - 2
        while n!=page+3:
            show_pages.append(n)
            n+=1
    return show_pages

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    query = session.query(Post).order_by(Post.date_posted.desc())
    posts = Paginator(query, 5)
    if page > posts.pages_range[-1]:
        return render_template("error.html", error = '404')
    posts_page = posts.page(page)
    show_pages = pagination(page, posts.pages_range)
    return render_template('home.html', posts_page=posts_page, posts=posts, show_pages=show_pages)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password=hashed_password)
        session.add(user)
        session.commit()
        # flash('Account created for {}!'.format(form.username.data), 'success')
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user =  session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            # flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['POST','GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
            os.remove(picture_path) 
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        session.add(post)
        session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = session.query(Post).get(post_id)
    if post:
        return render_template('post.html',title=post.title,post=post)
    else:
        return render_template("404.html")

@app.route("/post/<int:post_id>/update", methods=['POST','GET'])
@login_required
def update_post(post_id):
    post = session.query(Post).get(post_id)
    if post:
        if post.author != current_user:
            return render_template("error.html", error = '403')
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            session.commit()
            flash('Your post has been updated!','success')
            return redirect(url_for('post', post_id=post.id))
        elif request.method=='GET':
            form.title.data=post.title
            form.content.data=post.content
        return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")
    else:
        return render_template("error.html", error = '404')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = session.query(Post).get(post_id)
    if post:
        if post.author != current_user:
            return render_template("error.html", error = '403')
        session.delete(post)
        session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template("error.html", error = '404')

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return render_template("error.html", error = '404')
    query = session.query(Post).filter_by(author=user).order_by(Post.date_posted.desc())
    posts = Paginator(query, 5)
    if page > posts.pages_range[-1]:
        return render_template("error.html", error = '404')
    posts_page = posts.page(page)
    show_pages = pagination(page, posts.pages_range)
    return render_template('user_posts.html', query=query, posts_page=posts_page, posts=posts, show_pages=show_pages, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = ''' To reset your password, visit the following link:
{}

If you did not make this request then simple ignore this email and no changes will be made.
                '''.format(url_for('reset_token',token=token, _external=True))
    mail.send(msg)

@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset the password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        session.commit()
        flash('Your password has been updated! You are now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password", form=form)

