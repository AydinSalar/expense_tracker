import os

class Config:
    # Secret key for securely signing the session cookie and other security-related needs
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')  
    # Database URI; defaults to a local SQLite database if no DATABASE_URL environment variable is set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')  
    # Disable SQLAlchemy's event-driven modification tracking for performance reasons
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
