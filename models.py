from . import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),  nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable = False)
    rollno = db.Column(db.String(120), nullable =False)

    def __repr__(self):
        return f"User('{self.username}' , '{self.email}' , '{self.password}' , '{self.rollno}' )"

