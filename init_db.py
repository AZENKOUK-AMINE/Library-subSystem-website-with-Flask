"""
Script to initialize the database with new tables.
Run this script after adding new models to create the database tables.
"""
from library import app, db

with app.app_context():
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")
    print("New tables added: Reservation, Feedback")
