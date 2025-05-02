from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    username=StringField(label='Name', validators=[DataRequired()])
    student_id=IntegerField(label='ID', validators=[DataRequired()])
    passport_id=StringField(label='PassportID', validators=[DataRequired()])
    classs=StringField(label='Class', validators=[DataRequired()])
    type=SelectField(label='Type', validators=[DataRequired()] , choices=[('student', 'Student'), ('teacher', 'Teacher'), ('admin', 'Admin')])
    gender=SelectField(label='Gender', validators=[DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')])
    submit=SubmitField(label='Submit')
    
    