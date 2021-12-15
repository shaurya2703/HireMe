from library.text_similarity import similarity
from models import *
from enum import unique
import hashlib
import os
from cv2 import perspectiveTransform
from flask import Flask, render_template, session, request, redirect, url_for, flash, jsonify
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, login_user, LoginManager, login_required, logout_user, current_user
import hashlib
from werkzeug.utils import secure_filename
from ml_video_emotion import videoEmotion,videoToText

# from flask_script import Manager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hireMe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

db = SQLAlchemy(app)


UPLOAD_FOLDER = 'documents/videos'
ALLOWED_EXTENSIONS = {'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# migrate = Migrate(app,db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Login manager
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


@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        collegeName = request.form['collegeName']
        rollno = request.form['rollNo']
        password = request.form['password']
        new_student = Student(
            name=name, email=email, collegeName=collegeName, rollno=rollno, password=password)
        db.session.add(new_student)
        db.session.commit()
        print(new_student.name + " " + new_student.email +
              " " + new_student.collegeName)
        return redirect(url_for("student_login"))
    else:
        return render_template('student/accounts/signup.html')


@app.route('/student_login', methods=["POST", "GET"])
def student_login():
    if request.method == "POST":
        std_email = request.form['student_email']
        std_pass = request.form['student_pass']
        curr_student = Student.query.filter_by(email=std_email).first()
        if curr_student:
            if std_pass == curr_student.password:
                login_user(curr_student)
                session["account_type"] = 'Student'
                session["id"] = curr_student.id
                print(curr_student.name + " " + curr_student.password)
                return redirect(url_for("student_page"))
            else:
                print("Incorrect Password")
                return redirect(url_for("student_login"))
        else:
            print("Not found in database")
            return redirect(url_for("student_login"))
    else:
        if session.get("id"):
            return redirect(url_for("student_page"))
        return render_template('student/accounts/login.html')


@app.route('/student_logout', methods=['GET', 'POST'])
@login_required
def student_logout():
    # session["account_type"] = None
    session.pop("account_type", None)
    session.pop("id", None)
    logout_user()
    print("Student Logged out")
    return redirect(url_for('index'))


@app.route('/interviewer_signup', methods=["POST", "GET"])
def interviewer_signup():
    if request.method == 'POST':
        intvw_name = request.form['interviewer_name']
        intvw_email = request.form['interviewer_email']
        company_name = request.form['company_name']
        intvw_pass = request.form['interviewer_pass']
        new_interviewer = Interviewer(
            name=intvw_name, email=intvw_email, company_name=company_name, password=intvw_pass)
        db.session.add(new_interviewer)
        db.session.commit()
        print(new_interviewer.name + " " + new_interviewer.email +
              " " + new_interviewer.company_name)
        return redirect(url_for("interviewer_login"))
    else:
        return render_template('interviewer/accounts/signup.html')


@app.route('/interviewer_login', methods=["POST", "GET"])
def interviewer_login():
    if request.method == "POST":
        intvw_email = request.form['interviewer_email']
        intvw_pass = request.form['interviewer_pass']

        session["account_type"] = 'Interviewer'
        curr_interviewer = Interviewer.query.filter_by(
            email=intvw_email).first()
        if curr_interviewer:
            if intvw_pass != curr_interviewer.password:
                flash("Incorrect password")
            login_user(curr_interviewer)
        return redirect(url_for("interview_page"))
    else:
        return render_template('interviewer/accounts/login.html')


@app.route('/interviewer_logout', methods=['GET', 'POST'])
@login_required
def interviewer_logout():
    # session["account_type"] = None
    session.pop("account_type", None)
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
    result = db.session.execute(
        f'select i.name u,i.company_name cn,j.job_profile jp , j.job_id jid ,js.attempted att from interviewer i join jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id  where js.stu_id={ student_id } ')
    return render_template('student/dashboard.html', name=current_user.name, jobs_list=result)
    # else:
    #     return redirect(url_for("student_login"))


@app.route("/std/interview", methods=['GET', 'POST'])
@login_required
def student_interview():
    if request.method == 'GET':
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
        if q_no >= questions_list.count():
            # db.session.execute(f'''update job_stu_map set attempted=true where job_id={job_id} and 
            # stu_id={student_id}''')
            return redirect(url_for('student_page'))
        print(questions_list[q_no].question)
        question = questions_list[q_no].question
        q_id = questions_list[q_no].question_id
        # for _ in questions_list:
        #     pass
        return render_template('student/includes/std_interview.html', name=current_user.name,
                               job_id=job_id, ques=question, q_no=q_no+1,
                               q_id=q_id)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/std/video", methods=['GET', 'POST'])
@login_required
def upload_file():
    global UPLOAD_FOLDER
    predictions=dict()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        job_id = request.form['job_id']
        q_no = request.form['q_no']
        q_id = request.form['q_id']
        print(file.filename)
        print(job_id)
        print(q_no)
        print(q_id)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print("Starting to add video in db")
            full_path = "'"+UPLOAD_FOLDER+'/'+filename+"'"
            
            print(full_path[1:-1])
            cont=False
            
            predictions,cont = videoEmotion(full_path[1:-1])
            while not cont:
                print('inside while')
            print(predictions)
            print('video to text')
            text=videoToText(full_path[1:-1])
            #Correct answer
            print(text)
            correct_answer_path = Questions.query.filter_by(question_id = q_id).first().correct_answer_path
            with open(correct_answer_path,"r+" ) as file:
                correct_answer = file.read()
            print("Printing correct answers")    
            print(str(correct_answer))

            similarity_score= similarity(str(correct_answer),text)
            print(similarity_score)
            print(type(similarity_score))

            print(full_path)
            query = f''' insert into student_answers
            (question_id,stu_id,answer_path,anger_score,disgust_score,fear_score,happy_score,sad_score,surprise_score,neutral_score,similarity_score) 
            values ({q_id},{current_user.id},{full_path},{predictions[0]},{predictions[1]},{predictions[2]},{predictions[3]},{predictions[4]},{predictions[5]},{predictions[6]},{similarity_score}) '''
    #         
            print(query)
            db.session.execute(query)
            db.session.commit()
            db.session.execute(f'''update job_stu_map set attempted=true where job_id={job_id} and 
            stu_id={current_user.id}''')
            db.session.commit()

            print(text)
            print('commited')
            
       
        
    return url_for("student_interview" , job_id = job_id ,q_no = q_no ) 


@app.route("/std/job_openings")
@login_required
def job_openings():
    stu_id = session["id"]
    # company name ,job profile ,jd
    result = db.session.execute(f'''select j.job_id jid ,j.job_profile jp,j.job_description_path jd,i.company_name cname 
    from jobs j join interviewer i on j.interviewer_id =i.id
    where j.collegeName=(select s.collegeName from student s where s.id={stu_id})''')
    # join student s on s.collegeName=j.collegeName
    # where s.id={stu_id}''')

    table = []
    for i in result:
        temp = []
        temp.append(i.cname)
        temp.append(i.jp)
        with open(i.jd, 'r') as f:
            temp.append(f.read(50)+'...')
        temp.append(i.jid)
        temp.append(1 if Job_stu_map.query.filter_by(
            job_id=i.jid, stu_id=stu_id).first() else 0)
        table.append(temp)
        print(temp)
    return render_template('student/includes/job_openings.html', opening_list=table)


@app.route("/std/job_openings/enroll/<jid>")
@login_required
def enroll_job(jid):
    stu_id = session["id"]
    db.session.add(Job_stu_map(job_id=jid, stu_id=stu_id))
    db.session.commit()
    return redirect(url_for('job_openings'))


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
    table = []
    for i in result:
        temp = []
        temp.append(i.jp)
        with open(i.jd, 'r') as f:
            temp.append(f.read(50)+'...')
        temp.append(i.coll)
        temp.append(i.attempted)
        temp.append(i.jid)
        table.append(temp)
    print(table)

    return render_template('interviewer/dashboard.html', name=current_user.name, interviewer_id=current_user.id, table=table)
    # else:
    #     return redirect(url_for("interviewer_login"))


@app.route("/addquestion", methods=['GET', 'POST'])
@login_required
def addquestion():

    if request.method == "GET":

        jobid = request.args.get('job_id')
        job_profile = Jobs.query.filter_by(job_id=jobid).first().job_profile
        print(job_profile)
        return render_template("interviewer/includes/add_question.html", job_id=jobid, job_profile=job_profile)

    else:
        # jobid=request.args.get('job_id')
        question = request.form["question"]
        answer = request.form["answer"]
        jobid = request.form["job_id"]
        # print(question+answer+jobid)
        filepath = "documents/questions/" + \
            str(hashlib.sha1(bytes(question+str(jobid), 'utf-8')).hexdigest())+'.txt'
        with open(filepath, "w+") as file:
            file.write(answer)
        query=str(f'''insert into questions(question,correct_answer_path,job_id) 
        values('{question}','{filepath}','{jobid}')''')
        db.session.execute(query)
        db.session.commit()

        job_profile = Jobs.query.filter_by(job_id=jobid).first().job_profile
        print(job_profile)
        return render_template("interviewer/includes/add_question.html", job_id=jobid, job_profile=job_profile)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if request.method == 'POST':
        job_profile = request.form['job_profile']
        job_description = request.form['job_description']
        collegeName = request.form['collegeName']
        interviewer_id = request.args.get('interviewer_id')
        path_of_jobdesc = "documents/jobdesc/"
        filepath = path_of_jobdesc + \
            str(hashlib.sha1(bytes(job_description +
                str(interviewer_id), 'utf-8')).hexdigest())+'.txt'
        with open(filepath, "w+") as file:
            file.write(job_description)
        db.session.add(Jobs(job_profile=job_profile, job_description_path=filepath,
                            collegeName=collegeName,
                            interviewer=Interviewer.query.filter_by(
                                id=interviewer_id).first()
                            ))
        db.session.commit()
        return redirect(url_for("interview_page"))
    else:
        interviewer_id = request.args.get('interviewer_id')
        # print(interviewer_id)
        return render_template('interviewer/includes/add_Job.html', interviewer_id=interviewer_id)


@app.route('/show_scores', methods=['GET', 'POST'])
@login_required
def show_scores():
    interviewer_id = request.args.get('interviewer_id')
    job_id = request.args.get('job_id')
    return render_template('interviewer/includes/interview_scores.html', interviewer_id=interviewer_id, job_id=job_id)


if __name__ == '__main__':
    print("Creating tables")

    db.create_all()
    # manager.run()
    print("Tables created")
    db.session.execute('update job_stu_map set attempted=false')
    db.session.commit()
    # Student.query.all()
    app.run(port=5000, debug=True)
