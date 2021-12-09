from enum import unique
import hashlib
from flask import Flask,render_template, session,request, redirect, url_for, flash
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
import hashlib
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
        name = request.form['name']
        email = request.form['email']
        collegeName = request.form['collegeName']
        rollno = request.form['rollNo']
        password = request.form['password']
        new_student = Student(name = name, email = email ,collegeName=collegeName, rollno = rollno, password = password)
        db.session.add(new_student)
        db.session.commit()
        print(new_student.name + " " + new_student.email + " " + new_student.collegeName)
        return redirect(url_for("student_login"))
    else:    
        return render_template('student/accounts/signup.html')    

@app.route('/student_login', methods = ["POST","GET"])
def student_login():
    if request.method == "POST":
        std_email = request.form['student_email']
        std_pass = request.form['student_pass']
        curr_student = Student.query.filter_by(email=std_email).first()
        if curr_student:
            if std_pass == curr_student.password:
                login_user(curr_student)
                session["account_type"] = 'Student'
                session["id"]=curr_student.id
                print(curr_student.name + " "+ curr_student.password)
                return redirect(url_for("student_page"))
            else:
                print("Incorrect Password")
                return redirect(url_for("student_login"))
        else:
            print("Not found in database")
            return redirect(url_for("student_login"))
    else:
        if session.get("id") :
            return  redirect(url_for("student_page"))
        return render_template('student/accounts/login.html')


@app.route('/student_logout', methods = ['GET','POST'])
@login_required
def student_logout():
    # session["account_type"] = None
    session.pop("account_type",None)
    session.pop("id",None)
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
        new_interviewer = Interviewer(name = intvw_name, email = intvw_email ,company_name=company_name, password = intvw_pass)
        db.session.add(new_interviewer)
        db.session.commit()
        print(new_interviewer.name + " " + new_interviewer.email + " " + new_interviewer.company_name)
        return redirect(url_for("interviewer_login"))
    else:
        return render_template('interviewer/accounts/signup.html')

@app.route('/interviewer_login', methods = ["POST","GET"])
def interviewer_login():
    if request.method == "POST":
        intvw_email = request.form['interviewer_email']
        intvw_pass = request.form['interviewer_pass']

        session["account_type"] = 'Interviewer'
        curr_interviewer = Interviewer.query.filter_by(email=intvw_email).first()
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
        result = db.session.execute(f'select i.name u,i.company_name cn,j.job_profile jp , j.job_id jid from interviewer i join jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id where js.stu_id={ student_id }')
        return render_template('student/dashboard.html',name = current_user.name, jobs_list = result)
    # else:    
    #     return redirect(url_for("student_login"))

@app.route("/std/interview",methods=['GET','POST'])
@login_required
def student_interview():
    if request.method=='GET':
        print(current_user)
        print(current_user.id)
        student_id = current_user.id
        # intervw_list = Interviewer.query.all()
        job_id = request.args.get('job_id')
        q_no = int(request.args.get('q_no'))
        print(job_id)
        print((q_no))
        questions_list = Questions.query.filter_by(job_id=job_id)
        print(type(questions_list))
        if q_no>=questions_list.count():
            return redirect(url_for('student_page'))
        print(questions_list[q_no].question)
        return render_template('student/includes/std_interview.html', name = current_user.name, job_id = job_id,ques = questions_list[q_no].question,q_no = q_no+1 )

@app.route("/intvw")
@login_required
def interview_page():
    # if 'intvw_name' in session:
    #     name = session['intvw_name']
        print(current_user)
        print(current_user.id)
        
        result = db.session.execute(f'''
        select j.job_profile jp,j.job_description_path jd ,j.collegeName coll ,
        (SELECT count(*) from job_stu_map js where js.job_id=j.job_id and attempted=1) 
        attempted,j.job_id jid from  jobs j where interviewer_id={current_user.id} ; ''')
        table=[]
        for i in result:
            temp=[]
            temp.append(i.jp)
            with open(i.jd,'r') as f:
                temp.append(f.read(50)+'...')
            temp.append(i.coll)
            temp.append(i.attempted)
            temp.append(i.jid)
            table.append(temp)
        print (table)

        return render_template('interviewer/dashboard.html',name = current_user.name,interviewer_id=current_user.id, table=table)
    # else:    
    #     return redirect(url_for("interviewer_login"))
@app.route("/addquestion", methods = ['GET','POST'])
@login_required
def addquestion():
    
    if request.method=="GET":
        
        jobid=request.args.get('job_id')
        job_profile=Jobs.query.filter_by(job_id=jobid).first().job_profile
        print(job_profile)
        return render_template("interviewer/includes/add_question.html",job_id=jobid,job_profile=job_profile)
    
    else :
        # jobid=request.args.get('job_id')
        question=request.form["question"]
        answer=request.form["answer"]
        jobid=request.form["job_id"] 
        # print(question+answer+jobid)
        filepath="documents/questions/"+str(hashlib.sha1(bytes(question+str(jobid),'utf-8')).hexdigest())+'.txt'
        with open(filepath,"w+") as file:
            file.write(answer)
        # print(Jobs.query.filter_by(job_id=jobid).first())
        db.session.add(Questions(question=question,correct_answer_path=filepath
        ,jobs=Jobs.query.filter_by(job_id=jobid).first()))
        db.session.commit()

        job_profile=Jobs.query.filter_by(job_id=jobid).first().job_profile
        print(job_profile)
        return render_template("interviewer/includes/add_question.html",job_id=jobid,job_profile=job_profile)

# @app.route("/addlastquestion", methods = ['POST'])
# # @login_required
# def addlastquestion():
    
#     jobid=request.jobid
#     question=request.form.question
#     ans=request.answer
#     filepath=path_of_questions+str(hashlib.sha1(bytes(question+str(job.job_id),'utf-8')).hexdigest())+'.txt'
#     with open(filepath,"w+") as file:
#         file.write(ans)
#     db.session.add(Questions(question=question+'for'+str(job.job_id),correct_answer_path=filepath
#     ,jobs=job))
#     # result = db.session.execute(f'select i.name u,i.company_name cn,j.job_profile jp from interviewer i join 
#     # jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id where js.stu_id={ student_id }')
#     return render_template("interviewer/includes/add_question.html",job_id=jobid)




@app.route('/add_job', methods = ['GET','POST'])
@login_required
def add_job():
    if request.method == 'POST':
        job_profile = request.form['job_profile']
        job_description = request.form['job_description']
        collegeName = request.form['collegeName']
        interviewer_id = request.args.get('interviewer_id')
        path_of_jobdesc="documents/jobdesc/"
        filepath=path_of_jobdesc+str(hashlib.sha1(bytes(job_description+str(interviewer_id),'utf-8')).hexdigest())+'.txt' 
        with open(filepath,"w+") as file:
            file.write(job_description)
        db.session.add(Jobs(job_profile=job_profile,job_description_path=filepath,
        collegeName=collegeName,
        interviewer=Interviewer.query.filter_by(id=interviewer_id).first()
        ))
        db.session.commit()
        # print(new_job.job_profile + " " + new_job.job_description_path + " " + new_job.collegeName)
        # return render_template('interviewer/dashboard.html')
        return redirect(url_for("interview_page"))
    else:
        interviewer_id=request.args.get('interviewer_id')
        # print(interviewer_id)
        return render_template('interviewer/includes/add_Job.html',interviewer_id=interviewer_id)

if __name__ == '__main__':
    print("Creating tables")
    db.create_all()
    # manager.run()
    print("Tables created")
    # Student.query.all()
    app.run(port=5000,debug=True)