from flask import Flask,render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import url

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'HIRE_ME'

#session stores data as a dictionary

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/student_signup')
def student_signup():
    return render_template('student/signup.html')    

@app.route('/student_login', methods = ["POST","GET"])
def student_login():
    if request.method == "POST":
        session['std_name'] = request.form['student_name']
        session['std_pass'] = request.form['student_pass']
        return redirect(url_for("student_page"))
    else:
        return render_template('student/login.html')
    
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
def student_page():
    if 'std_name' in session:
        name = session['std_name']
        return f'Hello {name}'
    else:    
        return redirect(url_for("student_login"))

@app.route("/intvw")
def interview_page():
    if 'intvw_name' in session:
        name = session['intvw_name']
        return f'Hello {name}'
    else:    
        return redirect(url_for("interviewer_login"))

if __name__ == '__main__':
    app.run(port=5000,debug=True)

