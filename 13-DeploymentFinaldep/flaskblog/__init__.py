from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .config import Config
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Log environment variables for debugging
print(f"Loaded SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"Loaded SQLALCHEMY_DATABASE_URI: {os.getenv('SQLALCHEMY_DATABASE_URI')}")

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
admin = Admin()

# Custom admin view to limit access
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 1  # Only admins (role=1) can access

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)  # Return a 403 forbidden error if the user is not an admin

# Application factory function
def create_app(config_class=Config):
    app = Flask(__name__)

    # Load configuration from the config class
    app.config.from_object(config_class)

    # Print to verify the configuration
    print("SQLALCHEMY_DATABASE_URI is:", app.config.get('SQLALCHEMY_DATABASE_URI'))
    print("SECRET_KEY:", app.config.get('SECRET_KEY'))

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Import models to register with admin
    from .models import User, Post, Comment

    # Register Flask-Admin views with restricted access
    admin.init_app(app)
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Post, db.session))
    admin.add_view(AdminModelView(Comment, db.session))

    # Register Blueprints
    from .users.routes import users
    from .posts.routes import posts
    from .main.routes import main
    from .errors.handlers import errors
    from flaskblog.analytics.analytics_routes import analytics_bp  # Import your analytics blueprint

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(analytics_bp)  # Register your analytics blueprint here

    return app

