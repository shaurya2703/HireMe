-- SQLite
-- DELETE from job_stu_map ;
-- select i.username u,i.company_name cn,j.job_profile jp from interviewer i join jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id where js.stu_id=2
-- insert into Student_answers(question_id,stu_id,answer_path) values (2,3,3);
-- DELETE from student_answers;

-- select * from student_answers
-- insert into student_answers(question_id,stu_id,answer_path) values (3,2,'documents/videos/3Shaurya_Khanna1.mp4')

-- DELETE from student_answers
-- UPDATE job_stu_map set attempted = False
-- pragma table_info('student_answers');
-- insert into student_answers
--             (question_id,stu_id,answer_path,anger_score,disgust_score,fear_score,happy_score,sad_score,surprise_score,neutral_score,similarity_score) 
--             values (1,1,'111111',1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.5)
-- update job_stu_map set attempted=false

-- insert into jobs(job_profile,job_description_path,collegeName,interviewer_id) 
--             values('sample1','documents/jobdesc/9de5bea40088168742e2a1250759a494b420d56a.txt','tiet',1)

-- select s.name,avg(sa.anger_score),avg(sa.disgust_score),avg(sa.fear_score) ,avg(sa.happy_score),avg(sa.sad_score),avg(sa.surprise_score),avg(sa.neutral_score),avg(sa.similarity_score) 
--         from student_answers sa join questions q on q.question_id=sa.question_id  join student s on s.id=sa.stu_id where q.job_id= 1 group by stu_id

-- DELETE from jobs WHERE job_id = 5;