from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog import db
from flaskblog.models import Post, Comment
from flask_login import current_user
from .forms import CommentForm

comments = Blueprint('comments', __name__)

@comments.route("/post/<int:post_id>/comment", methods=['POST'])
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
    return redirect(url_for('main.post', post_id=post.id))
