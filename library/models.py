from library import db
from datetime import datetime

class Student(db.Model):
    
    name = db.Column(db.String(length=30), nullable=False )
    id = db.Column(db.Integer(), primary_key=True )
    passport = db.Column(db.Integer(), nullable=False , unique=True )
    classs = db.Column(db.String(length=30), nullable=False )
    type = db.Column(db.String(length=30), nullable=False )
    gender = db.Column(db.String(length=30), nullable=False )
    password = db.Column(db.String(length=30), nullable=False )
    
    
    def __repr__(self) :
        return f'Student {self.name}'
    
class Book(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True )
    title = db.Column(db.String(length=30), nullable=False)
    author = db.Column(db.String(length=30), nullable=False)
    type = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(length=80), nullable=False)
    image_path = db.Column(db.String(200))
    
    def __repr__(self) :
        return f'Book {self.title}'

class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)
    
  
    book = db.relationship('Book', backref='reservations')
    student = db.relationship('Student', backref='reservations')
    
    def __repr__(self):
        return f'Reservation {self.id}'

class Feedback(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
  
    student = db.relationship('Student', backref='feedbacks')
    
    def __repr__(self):
        return f'Feedback {self.id}'
    
    
    