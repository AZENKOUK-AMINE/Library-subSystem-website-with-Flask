from library import db
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
    
    
    