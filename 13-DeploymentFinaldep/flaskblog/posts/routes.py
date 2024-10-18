from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app, jsonify
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, PostLike
from flaskblog.posts.forms import PostForm, CommentForm
import os
import secrets
from PIL import Image

posts = Blueprint('posts', __name__)

def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = save_post_picture(form.image.data) if form.image.data else None
        post = Post(title=form.title.data, content=form.content.data, picture=image_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    form = CommentForm()
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments)

@posts.route("/post/<int:post_id>/comment", methods=['POST'])
@login_required
def comment_post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

@posts.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if post_like:
        if post_like.liked:
            db.session.delete(post_like)
        else:
            post_like.liked = True
    else:
        post_like = PostLike(user_id=current_user.id, post_id=post_id, liked=True)
        db.session.add(post_like)

    db.session.commit()

    likes_count = PostLike.query.filter_by(post_id=post_id, liked=True).count()
    dislikes_count = PostLike.query.filter_by(post_id=post_id, liked=False).count()

    return jsonify({'likes': likes_count, 'dislikes': dislikes_count})

@posts.route("/post/<int:post_id>/dislike", methods=['POST'])
@login_required
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    post_like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if post_like:
        if not post_like.liked:
            db.session.delete(post_like)
        else:
            post_like.liked = False
    else:
        post_like = PostLike(user_id=current_user.id, post_id=post_id, liked=False)
        db.session.add(post_like)

    db.session.commit()

    likes_count = PostLike.query.filter_by(post_id=post_id, liked=True).count()
    dislikes_count = PostLike.query.filter_by(post_id=post_id, liked=False).count()

    return jsonify({'likes': likes_count, 'dislikes': dislikes_count})

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_post_picture(form.image.data)
            post.picture = image_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/post/<int:post_id>/full_content', methods=['GET'])
def get_full_content(post_id):
    post = Post.query.get_or_404(post_id)
    return post.content

