from app import app  # Import the Flask app instance
from models import db  # Import the database instance from models

# Use the Flask application context to ensure database actions are tied to the app
with app.app_context():
    # Create all database tables based on models defined in the application
    db.create_all()
