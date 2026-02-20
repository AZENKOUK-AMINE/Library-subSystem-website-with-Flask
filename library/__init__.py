from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library.db'
app.config['SECRET_KEY']= '6586dd966221826fe6b1659c'
db =SQLAlchemy(app)
app.app_context().push()

from library import routes