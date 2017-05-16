from sqlite3 import connect
from hashlib import sha1
from os import urandom
import random,string

f = "data/tix.db"

def add_request(teacher,date,room,subject,body=None):
    db = connect(f)
    c = db.cursor()
    #create table requests if doesn't exist
    try:
        c.execute("SELECT * FROM requests")
    except:
        c.execute("CREATE TABLE requests (primary_key INT PRIMARY KEY AUTOINCREMENT, teacher_name TEXT, date_of_request TEXT, room_num INT, req_subject TEXT, req_body TEXT, tech_name TEXT, urgency INT, status INT)")
    query = ("INSERT INTO requests (teacher_name,date_of_request,room_num,req_subject,req_body) VALUES (?,?,?,?,?)")
    c.execute(query,(teacher,date,room,subject,body))
    db.commit()
    db.close()
