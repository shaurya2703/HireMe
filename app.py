from enum import unique
from flask import Flask,render_template, session,request, redirect, url_for, flash
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
# from flask_script import Manager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hireMe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

db  = SQLAlchemy(app)

from models import *
# migrate = Migrate(app,db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"



@login_manager.user_loader
def load_user(user_id):
  if session['account_type'] == 'Interviewer':
      return Interviewer.query.get(int(user_id))
  elif session['account_type'] == 'Student':
      print("Inside student loign session")
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
        collegeName = request.form['collegeName']
        rollno = request.form['rollNo']
        password = request.form['password']
        new_student = Student(username = username, email = email ,collegeName=collegeName, rollno = rollno, password = password)
        db.session.add(new_student)
        db.session.commit()
        print(new_student.username + " " + new_student.email + " " + new_student.collegeName)
        return redirect(url_for("student_login"))
    else:    
        return render_template('student/accounts/signup.html')    

@app.route('/student_login', methods = ["POST","GET"])
def student_login():
    if request.method == "POST":
        std_name = request.form['student_name']
        std_pass = request.form['student_pass']
        session["account_type"] = 'Student'
        curr_student = Student.query.filter_by(username=std_name).first()
        if curr_student:
            if std_pass == curr_student.password:
                login_user(curr_student)
                print(curr_student.username + " "+ curr_student.password)
                return redirect(url_for("student_page"))
            else:
                print("Incorrect Password")
                return redirect(url_for("student_login"))
        else:
            print("Not found in database")
            return redirect(url_for("student_login"))
    else:
        return render_template('student/accounts/login.html')


@app.route('/student_logout', methods = ['GET','POST'])
@login_required
def student_logout():
    # session["account_type"] = None
    session.pop("account_type",None)
    logout_user()
    print("Student Logged out")
    return redirect(url_for('index'))
    
@app.route('/interviewer_signup',methods = ["POST","GET"])
def interviewer_signup():
    if request.method == 'POST':
        intvw_name = request.form['interviewer_name']
        intvw_email = request.form['interviewer_email']
        company_name = request.form['company_name']
        intvw_pass = request.form['interviewer_pass']
        new_interviewer = Interviewer(username = intvw_name, email = intvw_email ,company_name=company_name, password = intvw_pass)
        db.session.add(new_interviewer)
        db.session.commit()
        print(new_interviewer.username + " " + new_interviewer.email + " " + new_interviewer.company_name)
        return redirect(url_for("interviewer_login"))
    else:
        return render_template('interviewer/accounts/signup.html')

@app.route('/interviewer_login', methods = ["POST","GET"])
def interviewer_login():
    if request.method == "POST":
        intvw_name = request.form['interviewer_name']
        intvw_pass = request.form['interviewer_pass']
        session["account_type"] = 'Interviewer'
        curr_interviewer = Interviewer.query.filter_by(username=intvw_name).first()
        if curr_interviewer:
            if intvw_pass != curr_interviewer.password:
                flash("Incorrect password")
            login_user(curr_interviewer)
        return redirect(url_for("interview_page"))
    else:
        return render_template('interviewer/accounts/login.html')

@app.route('/interviewer_logout', methods = ['GET','POST'])
@login_required
def interviewer_logout():
    # session["account_type"] = None
    session.pop("account_type",None)
    logout_user()
    print("Interviewer Logged out")
    return redirect(url_for('index'))

@app.route("/std")
@login_required
def student_page():
    # if 'std_name' in session:
    #     name = session['std_name']
        print(current_user)
        print(current_user.id)
        student_id = current_user.id
        # intervw_list = Interviewer.query.all()
        result = db.session.execute(f'select i.username u,i.company_name cn,j.job_profile jp from interviewer i join jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id where js.stu_id={ student_id }')
        return render_template('student/dashboard.html',name = current_user.username, jobs_list = result)
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
    print("Creating tables")
    db.create_all()
    # manager.run()
    print("Tables created")
    # Student.query.all()
    app.run(port=5000,debug=True)