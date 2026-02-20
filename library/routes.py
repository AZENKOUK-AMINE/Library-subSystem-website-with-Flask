from library import app
from flask import render_template,request,redirect,url_for,session,jsonify
from library.models import Student,Book,Reservation,Feedback
from library.forms import RegisterForm
from library import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime




@app.route('/books')
def main_page_books():
    books = Book.query.all()
    return render_template('main3.html', books=books)

@app.route('/borrowing-history')
def book_history():
    return render_template('bookHistoryUser.html')

@app.route('/feedback')
def feedback_page():
    return render_template('feedbackuser.html')

@app.route('/account')
def account_settings():
    
    user_data = {
        'id': session.get('user_id'),
        'name': session.get('user_name'),
        'type': session.get('user_type'),
        'gender': session.get('user_gender'),
        'passport': session.get('user_passport'),
        'classs': session.get('user_class')
    }
    return render_template('accountSettings.html', user=user_data)

@app.route('/api/books')
def get_books_api():
    books = Book.query.all()
    books_list = [{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'type': book.type,
        'description': book.description,
        'image': f'/static/uploads/{book.image_path}' if book.image_path else ''
    } for book in books]
    return {'books': books_list}

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_details.html', book=book)

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
        image_path = None  
        
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
              
                upload_dir = os.path.join('library','static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
              
                filename = secure_filename(image.filename)
                save_path = os.path.join(upload_dir, filename)
                image.save(save_path)
                
               
                image_path = filename  
        
        new_book = Book(
            title=request.form.get('title'),
            author=request.form.get('author'),
            type=request.form.get('type'),
            description=request.form.get('description'),
            image_path=image_path  
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
        
      
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
              
                upload_dir = os.path.join('library', 'static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                
                filename = secure_filename(image.filename)
                save_path = os.path.join(upload_dir, filename)
                image.save(save_path)
                
            
                book.image_path = filename
        
        db.session.commit()
        return redirect(url_for('books_history_page'))
    return render_template('addBook.html', book=book)

@app.route('/book/<int:id>/delete', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    

    if book.image_path:
        try:
            os.remove(os.path.join('static', 'uploads', book.image_path))
        except:
            pass
    
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books_history_page'))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('id')
        password = request.form.get('password')
        
       
        student = Student.query.filter_by(id=student_id).first()
        
        if student and student.password == password:
      
            session['user_id'] = student.id
            session['user_name'] = student.name
            session['user_type'] = student.type
            session['user_gender'] = student.gender
            session['user_passport'] = student.passport
            session['user_class'] = student.classs
            
           
            if student.type == 'Admin':
                return redirect(url_for('Admin_page'))
            else:
                return redirect(url_for('main_page_books'))
        else:
           
            return render_template('login.html', error='Invalid ID or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin/reservations')
def admin_reservations():
    return render_template('adminStudentsHistoryBooks.html')


@app.route('/api/reservations')
def get_reservations():
    reservations = Reservation.query.all()
    reservations_list = [{
        'id': res.id,
        'book_title': res.book.title,
        'book_author': res.book.author,
        'book_image': f'/static/uploads/{res.book.image_path}' if res.book.image_path else '',
        'student_name': res.student.name,
        'student_id': res.student.id,
        'start_time': res.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': res.end_time.strftime('%Y-%m-%d %H:%M:%S')
    } for res in reservations]
    return jsonify({'reservations': reservations_list})


@app.route('/admin/feedbacks')
def admin_feedbacks():
    return render_template('submittedFeedBacks.html')

@app.route('/api/feedbacks')
def get_feedbacks():
    feedbacks = Feedback.query.all()
    feedbacks_list = [{
        'id': fb.id,
        'username': fb.student.name,
        'userId': fb.student.id,
        'rating': fb.rating,
        'feedback': fb.feedback_text,
        'image': f'https://ui-avatars.com/api/?name={fb.student.name.replace(" ", "+")}&background={"4A90E2" if fb.student.gender == "Male" else "E91E63"}&color=fff&size=200',
        'created_at': fb.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for fb in feedbacks]
    return jsonify({'feedbacks': feedbacks_list})


@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    new_feedback = Feedback(
        student_id=session['user_id'],
        rating=data.get('rating'),
        feedback_text=data.get('feedback')
    )
    db.session.add(new_feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted successfully'}), 201


@app.route('/api/reserve-book', methods=['POST'])
def reserve_book():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    

    start_time_str = data.get('start_time')
    end_time_str = data.get('end_time')
    
    
    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
    
    try:
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
    
    new_reservation = Reservation(
        book_id=data.get('book_id'),
        student_id=session['user_id'],
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(new_reservation)
    db.session.commit()
    return jsonify({'message': 'Book reserved successfully'}), 201