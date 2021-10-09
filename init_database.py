from models import *
import hashlib
db.create_all()
'''populating student table'''

db.session.add(Student(name ='Satvik Mehra', email = 'satvik@gmail.com',collegeName='tiet', rollno = 3278, password = 'satvik'))
db.session.add(Student(name ='Shaurya Khanna', email = 'shaurya@gmail.com',collegeName='tiet', rollno = 3429, password = 'shaurya'))
db.session.add(Student(name ='Rohit Bhatia', email = 'rohit@gmail.com',collegeName='tiet', rollno = 3203, password = 'rohit'))
db.session.add(Student(name ='Parivansh Deep Singh', email = 'parivansh@gmail.com',collegeName='thapar', rollno = 3194, password = 'pari'))
db.session.commit()

'''populating interviewer table'''
db.session.add(Interviewer(name ='SM', email = 'satvik@gmail.com', company_name = 'UBS', password = 'satvik'))
db.session.add(Interviewer(name ='SK', email = 'shaurya@gmail.com', company_name = 'JP', password = 'shaurya'))
db.session.add(Interviewer(name ='RB', email = 'rohit@gmail.com', company_name = 'ION', password = 'rohit'))
db.session.add(Interviewer(name ='PDS', email = 'parivansh@gmail.com', company_name = 'PAYTM' ,password = 'pari'))
db.session.commit()

'''populating jobs table'''
path_of_jobdesc="documents/jobdesc/"
jd="this is the sample Job description for the given company just for debugging purpose "
for i in range(1,5):
    filepath=path_of_jobdesc+str(hashlib.sha1(bytes(jd+str(i),'utf-8')).hexdigest())+'.txt' 
    with open(filepath,"w+") as file:
        file.write(jd)
    db.session.add(Jobs(job_profile="sample"+str(i),job_description_path=filepath,
    collegeName='tiet' if i!=4 else 'thapar',
    interviewer=Interviewer.query.filter_by(id=i).first()
    ))

db.session.commit()

'''populating job_stu_map table'''

for stu in Student.query.all():
    for job in Jobs.query.filter_by(collegeName=stu.collegeName):
        db.session.add(Job_stu_map(jobs=job,student=stu))
db.session.commit()

'''populating questions table'''
path_of_questions='documents/questions/'
question="Sample question"
ans="this is a sample question and has no answer this is just for the debug and purpose and nothing more"
for job in Jobs.query.all():
    filepath=path_of_questions+str(hashlib.sha1(bytes(question+str(job.job_id),'utf-8')).hexdigest())+'.txt'
    with open(filepath,"w+") as file:
        file.write(ans)
    db.session.add(Questions(question=question+'for'+str(job.job_id),correct_answer_path=filepath
    ,jobs=job))

db.session.commit()
