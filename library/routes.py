from library import app
from flask import render_template,request,redirect,url_for
from library.models import Student,Book
from library.forms import RegisterForm
from library import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime




@app.route('/books')
def main_page_books():
    return render_template('main3.html')

@app.route('/borrowing-history')
def book_history():
    return render_template('bookHistoryUser.html')

@app.route('/User_Data')
def user_data():
    students=Student.query.all()
    return render_template('usersData.html' , students=students)

@app.route('/Adminmain')
def Admin_page():
    return render_template('Adminmain.html')


@app.route('/Books_data')
def books_history_page():
    books=Book.query.all()
    print("Debug - Books found:", books)
    print("ss")
    print("Number of books:", len(books))
    for i, book in enumerate(books, 1):
        print(f"Book {i}: {book.title} | Image Path: {book.image_path}")
    return render_template('bookHistory.html', books=books)


@app.route('/add book', methods=['GET', 'POST'])
def Add_book_page():
    if request.method == 'POST':
        image_path = None  # Initialize as None
        
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Ensure the uploads directory exists
                upload_dir = os.path.join('library','static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate secure filename and save
                filename = secure_filename(image.filename)
                save_path = os.path.join(upload_dir, filename)
                image.save(save_path)
                
                # Store ONLY the filename (not full path) in database
                image_path = filename  # Changed from os.path.join('uploads', filename)
        
        new_book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            type=request.form.get('type'),
            description=request.form.get('description'),
            image_path=image_path  # Now storing just the filename
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books_history_page'))
    
    return render_template('addBook.html')





@app.route('/User_data', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' :
        new_student = Student(
            name=request.form.get('Name'),
            id=request.form.get('ID'),
            passport=request.form.get('PassportID'),
            classs=request.form.get('class'),
            type=request.form.get('Type'),
            gender=request.form.get('Gender'),
            password="123456789"
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('user_data' ,_external=True))
      
    return render_template('usersData.html' ,form=form)




@app.route('/<int:id>/update', methods=['GET','POST'])  
def update(id):
    students = Student.query.filter_by(id=id).first()
    if request.method == 'POST':
        # Update student data from form submission
        students.name = request.form.get('Name')
        students.id=request.form.get('ID')
        students.passport = request.form.get('PassportID')
        students.classs = request.form.get('class')
        students.type = request.form.get('Type')
        students.gender = request.form.get('Gender')
        
        db.session.commit()
        
        return redirect(url_for('user_data'))
    
    return render_template('updateStudent.html', students=students)
    
@app.route('/<int:id>/delete', methods=['POST'])  
def delete(id):
    students = Student.query.get_or_404(id)
    db.session.delete(students)
    db.session.commit()
    return redirect(url_for('user_data'))


@app.route('/book/<int:id>/update', methods=['GET', 'POST'])
def update_book(id):
    book = Book.query.filter_by(id=id).first()
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.type = request.form.get('type')
        book.description = request.form.get('description')
        
        # Handle image update if needed
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Ensure the uploads directory exists
                upload_dir = os.path.join('library', 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate secure filename and save
                filename = secure_filename(image.filename)
                save_path = os.path.join(upload_dir, filename)
                image.save(save_path)
                
                # Update the book's image path
                book.image_path = filename
        
        db.session.commit()
        return redirect(url_for('books_history_page'))
    return render_template('addBook.html', book=book)

@app.route('/book/<int:id>/delete', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    
    # Optional: Delete the associated image file
    if book.image_path:
        try:
            os.remove(os.path.join('static', 'uploads', book.image_path))
        except:
            pass
    
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books_history_page'))