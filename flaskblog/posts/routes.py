from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from flaskblog.database import session
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts',__name__)

@posts.route("/post/new", methods=['POST','GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        session.add(post)
        session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = session.query(Post).get(post_id)
    if post:
        return render_template('post.html',title=post.title,post=post)
    else:
        return render_template("404.html")

@posts.route("/post/<int:post_id>/update", methods=['POST','GET'])
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
            return redirect(url_for('posts.post', post_id=post.id))
        elif request.method=='GET':
            form.title.data=post.title
            form.content.data=post.content
        return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")
    else:
        return render_template("error.html", error = '404')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = session.query(Post).get(post_id)
    if post:
        if post.author != current_user:
            return render_template("error.html", error = '403')
        session.delete(post)
        session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template("error.html", error = '404')