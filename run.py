from library import app , db

from library.models import Student, db
with app.app_context():
    db.create_all()
    
    

    
    
if __name__=='__main__':
    app.run(debug=True)
    
with app.app_context():
    students = Student.query.all()
    print(students)