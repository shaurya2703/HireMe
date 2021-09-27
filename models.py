from app import app as app
from app import db
from flask_login import UserMixin
# from flask_migrate import Migrate

# migrate = Migrate(app,db)

class Student(db.Model, UserMixin):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),  nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    collegeName = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable = False)
    rollno = db.Column(db.String(120), nullable =False)

    def __repr__(self):
        return f"User('{self.username}' , '{self.email}' , '{self.collegeName}' , '{self.password}' , '{self.rollno}' )"

class Interviewer(db.Model, UserMixin):
    __tablename__ = 'Interviewer' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),  nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    companyName = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable = False)

    def __repr__(self):
        return f"User('{self.username}' , '{self.email}' , '{self.companyName}' , '{self.password}')"
