from flask import Blueprint, render_template
from flask_login import login_required
from flaskblog.models import User, Post, Comment
from flaskblog.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    user_count = User.query.count()
    post_count = Post.query.count()
    comment_count = Comment.query.count()

    # For chart data
    posts_by_month = Post.query.with_entities(db.func.strftime('%Y-%m', Post.date_posted), db.func.count(Post.id)).group_by(db.func.strftime('%Y-%m', Post.date_posted)).all()
    
    # Prepare data for Chart.js
    months = [month for month, _ in posts_by_month]
    posts_per_month = [count for _, count in posts_by_month]

    return render_template('admin_dashboard.html', user_count=user_count, post_count=post_count, comment_count=comment_count, months=months, posts_per_month=posts_per_month)

