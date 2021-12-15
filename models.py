from flask.sessions import NullSession
from app import db
from flask_login import UserMixin

class Student(db.Model, UserMixin):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),  nullable=False)
    email = db.Column(db.String(120), nullable=False ,unique=True)
    password = db.Column(db.String(120),nullable = False)
    rollno = db.Column(db.String(120), nullable =False)
    collegeName= db.Column(db.String(120), nullable =False)
    jobs_enrolled=db.relationship('Job_stu_map',backref='student')
    # answers=db.relationship('Student_answers',backref='student')
    

    def __repr__(self):
        return (f"User(import '{self.name}' , '{self.email}' , '{self.password}' , '{self.rollno}' ,'{self.collegeName}')")

class Interviewer(db.Model, UserMixin):
    __tablename__ = 'interviewer' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),  nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120),nullable = False)
    company_name=db.Column(db.String(120),nullable=False)
    jobs_added=db.relationship('Jobs',backref='interviewer')

    def __repr__(self):
        return (f"User('{self.name}' , '{self.email}' , '{self.password}', '{self.company_name}')")

class Jobs(db.Model,UserMixin):
    __tablename__='jobs'
    job_id=db.Column(db.Integer, primary_key=True)
    job_profile=db.Column(db.String(120),nullable = False)
    job_description_path=db.Column(db.String(120),nullable = False)
    collegeName=db.Column(db.String(120), nullable =False)
    interviewer_id=db.Column(db.Integer, db.ForeignKey('interviewer.id'))
    questions_added=db.relationship('Questions',backref='jobs')
    stu_for_job=db.relationship('Job_stu_map',backref='jobs')

class Questions(db.Model,UserMixin):
    __tablename__='questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(120),  nullable=False)
    correct_answer_path = db.Column(db.String(120), nullable=False)
    job_id=db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    # student_answers=db.relationship('Student_answers',backref='questions')
    

class Job_stu_map(db.Model,UserMixin):
    __tablename__='job_stu_map'
    js_id = db.Column(db.Integer, primary_key=True)
    job_id=db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    stu_id=db.Column(db.Integer, db.ForeignKey('student.id'))
    attempted=db.Column(db.Boolean, default=False)

class Student_answers(db.Model,UserMixin):
    __tablename__='student_answers'
    answer_id = db.Column(db.Integer, primary_key=True)
    question_id=db.Column(db.Integer, nullable=False)
    stu_id=db.Column(db.Integer, nullable=False)
    answer_path=db.Column(db.String(120), nullable=False)
    anger_score = db.Column(db.Float,nullable = False)
    disgust_score  = db.Column(db.Float,nullable = False)
    fear_score = db.Column(db.Float,nullable = False)
    happy_score = db.Column(db.Float,nullable = False)
    sad_score = db.Column(db.Float,nullable = False)
    surprise_score = db.Column(db.Float,nullable = False)
    neutral_score = db.Column(db.Float,nullable = False)
    similarity_score = db.Column(db.Float,nullable = False)


'''def Student_scores(db.Model,UserMixin):
    __tablename__='student_scored'
    job_id=db.Column(db.Integer, nullable=False)
    stu_id=db.Column(db.Integer, nullable=False)'''
    #can be the same table as jobs_for students
    