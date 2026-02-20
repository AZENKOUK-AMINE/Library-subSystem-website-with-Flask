# Library Management System - Update Notes

## Recent Changes

### Fixed Issues
1. **User History Page (Reservations)** - Now displays data from the database instead of localStorage
2. **Submitted Feedbacks Page** - Now displays data from the database instead of localStorage

### New Features Added

#### 1. Database Models
- **Reservation Model**: Tracks book reservations with start/end times
  - Links books to students
  - Stores reservation dates
  
- **Feedback Model**: Stores user feedback submissions
  - Stores rating (1-5 stars)
  - Stores feedback text
  - Links to the student who submitted it
  - Timestamps when feedback was submitted

#### 2. New API Routes

##### Admin Routes:
- `GET /admin/reservations` - View all book reservations page
- `GET /admin/feedbacks` - View all submitted feedbacks page

##### API Endpoints:
- `GET /api/reservations` - Get all reservations as JSON
- `GET /api/feedbacks` - Get all feedbacks as JSON
- `POST /api/submit-feedback` - Submit new feedback (requires login)
- `POST /api/reserve-book` - Reserve a book (requires login)

#### 3. Updated Pages

##### adminStudentsHistoryBooks.html
- Now fetches reservation data from `/api/reservations`
- Displays book details, student info, and reservation times
- Shows error messages if data cannot be loaded

##### submittedFeedBacks.html
- Now fetches feedback data from `/api/feedbacks`
- Displays user ratings and feedback text
- Shows message if no feedback exists

##### feedbackuser.html
- Now submits feedback to server via `/api/submit-feedback`
- Validates rating and feedback text before submission
- Clears form after successful submission

##### Adminmain.html
- Updated links to use Flask url_for() routing
- Properly links to new reservation and feedback pages

### How to Test

1. **Test Feedback Submission:**
   - Login as a regular user
   - Navigate to Feedback page
   - Select a star rating and enter feedback text
   - Click "Submit Feedback"
   - Login as admin and check "submittedFeedBacks" page

2. **Test Reservation Display:**
   - Login as admin
   - Go to "Users Borrowing History"
   - View reservation data (initially empty until reservations are created)

### Adding Test Data

To add test reservations and feedback, you can use Python console:

```python
from library import app, db
from library.models import Student, Book, Reservation, Feedback
from datetime import datetime, timedelta

with app.app_context():
    # Create a test reservation
    student = Student.query.first()
    book = Book.query.first()
    
    if student and book:
        reservation = Reservation(
            book_id=book.id,
            student_id=student.id,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(days=7)
        )
        db.session.add(reservation)
        
        # Create test feedback
        feedback = Feedback(
            student_id=student.id,
            rating=5,
            feedback_text="Great library system!"
        )
        db.session.add(feedback)
        
        db.session.commit()
        print("Test data added!")
```

### Technical Details

- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript with Fetch API
- **Backend**: Flask Python framework
- **Data Flow**: Client → API Endpoint → Database → JSON Response → Client Display

### Migration Notes

All existing localStorage-based functionality has been replaced with server-side database storage. This ensures:
- Data persistence across sessions and browsers
- Multi-user data sharing
- Better security and data integrity
- Centralized data management
