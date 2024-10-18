from flask import current_app
from .import db, login_manager
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)  # Track email confirmation
    role = db.Column(db.Integer, default=0)  # 0: Regular User, 1: Admin User
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # New field

    # Token generation for email confirmation
    def get_confirm_token(self, expires_sec=1800):
        """Generates a token for email confirmation."""
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')  # Ensure SECRET_KEY is bytes
        s = Serializer(secret_key)
        return s.dumps({'user_id': self.id})  # No need to decode

    @staticmethod
    def verify_confirm_token(token):
        """Verifies the token for email confirmation."""
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')  # Ensure SECRET_KEY is bytes
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    # Token generation for password reset
    def get_reset_token(self, expires_sec=1800):
        """Generates a token to reset the password for a user."""
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')  # Ensure SECRET_KEY is bytes
        s = Serializer(secret_key)
        return s.dumps({'user_id': self.id})  # No need to decode

    @staticmethod
    def verify_reset_token(token):
        """Verifies the token to reset the password."""
        secret_key = current_app.config['SECRET_KEY']
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')  # Ensure SECRET_KEY is bytes
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def has_liked_post(self, post):
        """Checks if a user has liked a post."""
        return PostLike.query.filter_by(user_id=self.id, post_id=post.id, liked=True).first() is not None

    def has_disliked_post(self, post):
        """Checks if a user has disliked a post."""
        return PostLike.query.filter_by(user_id=self.id, post_id=post.id, liked=False).first() is not None

    def is_admin(self):
        """Returns True if the user is an admin."""
        return self.role == 1

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    post_likes = db.relationship('PostLike', backref='post', lazy=True)

    @property
    def like_count(self):
        """Returns the number of likes for the post."""
        return PostLike.query.filter_by(post_id=self.id, liked=True).count()

    @property
    def dislike_count(self):
        """Returns the number of dislikes for the post."""
        return PostLike.query.filter_by(post_id=self.id, liked=False).count()

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"


class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    liked = db.Column(db.Boolean, nullable=False)  # True for like, False for dislike

    def __repr__(self):
        return f"PostLike(User ID: {self.user_id}, Post ID: {self.post_id}, Liked: {self.liked})"

