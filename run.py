from library import app, db
from library.models import Student

with app.app_context():
    db.create_all()
    
   
    test_admin = Student.query.filter_by(id=1).first()
    if not test_admin:
        test_admin = Student(
            id=1,
            name='Admin User',
            passport='ADMIN001',
            classs='N/A',
            type='Admin',
            gender='Male',
            password='admin123'
        )
        db.session.add(test_admin)
        db.session.commit()
        print("Test admin created: ID='1', Password='admin123'")
    
    
    students = Student.query.all()
    print("\n=== Current Users in Database ===")
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Type: {student.type}, Password: {student.password}")
    print("=================================\n")

if __name__ == '__main__':
    app.run(debug=True)