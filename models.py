from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# User model to represent users in the application
class User(UserMixin, db.Model):
    # Primary key for user
    id = db.Column(db.Integer, primary_key=True)
    # Unique username field
    username = db.Column(db.String(150), unique=True, nullable=False)
    # Unique email field
    email = db.Column(db.String(150), unique=True, nullable=False)
    # Password hash for securely storing passwords
    password_hash = db.Column(db.String(128), nullable=False)

    # Define a one-to-many relationship between User and Expense
    expenses = db.relationship('Expense', backref='user', lazy=True)

# Expense model to represent user expenses
class Expense(db.Model):
    # Primary key for expense
    id = db.Column(db.Integer, primary_key=True)
    # Foreign key to link the expense to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Amount for the expense
    amount = db.Column(db.Float, nullable=False)
    # Category for the expense (e.g., Food, Transport)
    category = db.Column(db.String(50), nullable=False
