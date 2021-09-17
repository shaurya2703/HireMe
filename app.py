from enum import unique
from flask import Flask,render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from .models import Student

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hireMe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db  = SQLAlchemy(app)


#Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_student(user_id):
    return Student.query.get(int(user_id))


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
        student = Student.query.filter_by(username=std_name).first()
        if student:
            if std_pass != student.password:
                flash("Incorrect password")
                # return render_template('student/login.html')
            login_user(student)

        # cur = db.connection.cursor()
        # cur.execute("INSERT INTO students(name, email, password, rollno) VALUES (%s,%s,%s,%s)",(std_name,'test@test.com',std_pass, '123456'))
        # db.connection.commit()
        # cur.close()
        return redirect(url_for("student_page"))
    else:
        return render_template('student/login.html')


@app.route('/student_logout', methods = ['GET','POST'])
@login_required
def student_logout():
    logout_user()
    print("Student Logged out")
    return redirect(url_for('student_login'))
    
@app.route('/interviewer_signup',methods = ["POST","GET"])
def interviewer_signup():
    if request.method == "POST":
        session['intvw_name'] = request.form['interviewer_name']
        session['intvw_email'] = request.form['interviewer_email']
        session['intvw_pass'] = request.form['interviewer_pass']
        session['intvw_re_pass'] = request.form['interviewer_re_pass']
        if(session['intvw_pass'] == session['intvw_re_pass']):
            print("true")
            return redirect(url_for("interview_page"))
        else:
            print("false")
            return render_template('interviewer/signup.html')
    else:
        return render_template('interviewer/signup.html')   

@app.route('/interviewer_login', methods = ["POST","GET"])
def interviewer_login():
    if request.method == "POST":
        session['intvw_name'] = request.form['interviewer_name']
        session['intvw_pass'] = request.form['interviewer_pass']
        return redirect(url_for("interview_page"))
    else:
        return render_template('interviewer/login.html')

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
def interview_page():
    if 'intvw_name' in session:
        name = session['intvw_name']
        return f'Hello {name}'
    else:    
        return redirect(url_for("interviewer_login"))

if __name__ == '__main__':
    db.create_all()
    app.run(port=5000,debug=True)

