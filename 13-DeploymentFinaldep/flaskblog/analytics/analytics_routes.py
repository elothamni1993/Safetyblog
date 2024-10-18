from flask import Blueprint, render_template
from flask_login import login_required
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from sqlalchemy import func
from flaskblog import db
from flaskblog.models import User, Post, Comment

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
@login_required
def analytics_home():
    # Overall statistics
    user_count = User.query.count()
    post_count = Post.query.count()
    comment_count = Comment.query.count()

    # User growth over time
    user_growth = db.session.query(
        func.date(User.date_registered),
        func.count(User.id)
    ).group_by(func.date(User.date_registered)).all()

    user_growth_dates = [str(entry[0]) for entry in user_growth]
    user_growth_counts = [entry[1] for entry in user_growth]

    # Post activity by day of the week
    post_activity = db.session.query(
        func.extract('dow', Post.date_posted),  # Extracts day of the week (0 = Sunday, 6 = Saturday)
        func.count(Post.id)
    ).group_by(func.extract('dow', Post.date_posted)).all()

    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    post_activity_by_day = [0] * 7  # Initialize all days with 0
    for day, count in post_activity:
        post_activity_by_day[int(day)] = count

    # Comment activity by hour of the day
    comment_activity = db.session.query(
        func.extract('hour', Comment.date_posted),
        func.count(Comment.id)
    ).group_by(func.extract('hour', Comment.date_posted)).all()

    comment_activity_by_hour = [0] * 24  # Initialize all hours with 0
    for hour, count in comment_activity:
        comment_activity_by_hour[int(hour)] = count

    # User engagement (Active vs Inactive users)
    active_users = db.session.query(User.id).join(Post).distinct().count()
    inactive_users = user_count - active_users

    return render_template('analytics/dashboard.html',
                           user_count=user_count, 
                           post_count=post_count, 
                           comment_count=comment_count,
                           user_growth_dates=user_growth_dates,
                           user_growth_counts=user_growth_counts,
                           post_activity_by_day=post_activity_by_day,
                           comment_activity_by_hour=comment_activity_by_hour,
                           active_users=active_users,
                           inactive_users=inactive_users)

