-- SQLite
-- DELETE from job_stu_map ;
-- select i.username u,i.company_name cn,j.job_profile jp from interviewer i join jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id where js.stu_id=2
-- insert into Student_answers(question_id,stu_id,answer_path) values (2,3,3);
DELETE from student_answers;

-- select * from student_answers
-- insert into student_answers(question_id,stu_id,answer_path) values (3,2,'documents/videos/3Shaurya_Khanna1.mp4')

-- DELETE from student_answers
-- UPDATE job_stu_map set attempted = False
-- pragma table_info('student_answers');
-- insert into student_answers
--             (question_id,stu_id,answer_path,anger_score,disgust_score,fear_score,happy_score,sad_score,surprise_score,neutral_score,similarity_score) 
--             values (1,1,'111111',1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.5)
-- update job_stu_map set attempted=false


