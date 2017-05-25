import csv
from sqlite3 import connect

f = "data/tix.db"

with open('data/archive.csv','w') as csvfile:
    fieldnames = ['ID','teacher_username','teacher_name','submission_time','room_number','issue','description','teacher_name','tech_name','urgency','status']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    writer.writerow({'status':2,'urgency':1,'submission_time':"mmddyy",'issue':2, 'teacher_name':"teacher1",'tech_name':"tech1"})
