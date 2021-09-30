-- SQLite
select i.username u,i.company_name cn,j.job_profile jp from interviewer i join jobs j on j.interviewer_id = i.id join job_stu_map js on js.job_id=j.job_id where js.stu_id=2