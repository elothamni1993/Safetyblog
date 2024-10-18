import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'

    # Use PostgreSQL provided by Heroku if available, otherwise fallback to SQLite
    # Modify DATABASE_URL to replace 'postgres://' with 'postgresql://'
    uri = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'site.db')
    if uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = uri

    # Track modifications (set to False to avoid overhead)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gmail SMTP settings for sending emails
    MAIL_SERVER = 'smtp.gmail.com'  # Gmail SMTP server
    MAIL_PORT = 587  # Gmail SMTP port
    MAIL_USE_TLS = True  # TLS encryption
    MAIL_USE_SSL = False  # Do not use SSL
    MAIL_USERNAME = os.environ.get('EMAIL_USER')  # Your Gmail address
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  # Your Gmail app password
    MAIL_DEBUG = True  # Enable debug mode for email sending
    STATIC_FOLDER = 'static'

