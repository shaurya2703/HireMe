from enum import unique
from flask import Flask,render_template, session,request, redirect, url_for, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from models import *
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hireMe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db  = SQLAlchemy(app)


#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
  if session['account_type'] == 'Interviewer':
      return Interviewer.query.get(int(user_id))
  elif session['account_type'] == 'Student':
      return Student.query.get(int(user_id))
  else:
      return None
# @login_manager.user_loader
# def load_interviewer(user_id):
#     return Interviewer.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return "You are not logged in"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/student_signup', methods = ['GET','POST'])
def student_signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        rollno = request.form['rollNo']
        password = request.form['password']
        student = Student(username = username, email = email , rollno = rollno, password = password)
        db.session.add(student)
        db.session.commit()
        print(student.username + " " + student.email)
        return redirect(url_for("student_login"))
    else:    
        return render_template('student/signup.html')    

@app.route('/student_login', methods = ["POST","GET"])
def student_login():
    if request.method == "POST":
        std_name = request.form['student_name']
        std_pass = request.form['student_pass']
        session["account_type"] = 'Student'
        student = Student.query.filter_by(username=std_name).first()
        if student:
            if std_pass == student.password:
                login_user(student)
                return redirect(url_for("student_page"))
            else:
                print("Incorrect Password")
                return redirect(url_for("student_login"))
    else:
        return render_template('student/login.html')


@app.route('/student_logout', methods = ['GET','POST'])
@login_required
def student_logout():
    session["account_type"] = None
    logout_user()
    print("Student Logged out")
    return redirect(url_for('student_login'))
    
@app.route('/interviewer_signup',methods = ["POST","GET"])
def interviewer_signup():
    if request.method == 'POST':
        intvw_name = request.form['interviewer_name']
        intvw_email = request.form['interviewer_email']
        intvw_pass = request.form['interviewer_pass']
        interviewer = Interviewer(username = intvw_name, email = intvw_email , password = intvw_pass)
        db.session.add(interviewer)
        db.session.commit()
        print(interviewer.username + " " + interviewer.email)
        return redirect(url_for("interviewer_login"))
    else:    
        return render_template('interviewer/signup.html')

@app.route('/interviewer_login', methods = ["POST","GET"])
def interviewer_login():
    if request.method == "POST":
        intvw_name = request.form['interviewer_name']
        intvw_pass = request.form['interviewer_pass']
        session["account_type"] = 'Interviewer'
        interviewer = Interviewer.query.filter_by(username=intvw_name).first()
        if interviewer:
            if intvw_pass != interviewer.password:
                flash("Incorrect password")
            login_user(interviewer)
        return redirect(url_for("interview_page"))
    else:
        return render_template('interviewer/login.html')

@app.route('/interviewer_logout', methods = ['GET','POST'])
@login_required
def interviewer_logout():
    session["account_type"] = None
    logout_user()
    print("Interviewer Logged out")
    return redirect(url_for('interviewer_login'))

@app.route("/std")
@login_required
def student_page():
    # if 'std_name' in session:
    #     name = session['std_name']
        print(current_user)
        print(current_user.id)
        return render_template('student/dashboard.html',name = current_user.username)
    # else:    
    #     return redirect(url_for("student_login"))

@app.route("/intvw")
@login_required
def interview_page():
    # if 'intvw_name' in session:
    #     name = session['intvw_name']
        print(current_user)
        print(current_user.id)
        return render_template('interviewer/dashboard.html',name = current_user.username)
    # else:    
    #     return redirect(url_for("interviewer_login"))

if __name__ == '__main__':
    # db.create_all()
    app.run(port=5000,debug=True)

