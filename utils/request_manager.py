from sqlite3 import connect
from hashlib import sha1
from os import urandom
import random,string

f = "data/tix.db"

#-----------------------------
# Teacher create request
#-----------------------------
def add_request(teacher,date,room,subject,body=None):
    db = connect(f)
    c = db.cursor()
    #select table requests, create table requests if doesn't exist
    try:
        c.execute("SELECT * FROM requests")
    except:
        c.execute("CREATE TABLE requests (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, teacher_name TEXT, date_of_request TEXT, room_num INT, req_subject TEXT, req_body TEXT, tech_name TEXT, urgency INT, status INT)")

    #create request entry with given info
    query = ("INSERT INTO requests (teacher_name,date_of_request,room_num,req_subject,req_body) VALUES (?,?,?,?,?)")
    c.execute(query,(teacher,date,room,subject,body))
    db.commit()
    db.close()
    return "Request created!"

#---------------------------
# Tech accept request
#---------------------------
def accept_request(key,tech,urgency,status):
    db = connect(f)
    c = db.cursor()

    #find request with given primary key
    query = ("SELECT * FROM requests WHERE primary_key=?")
    request = c.execute(query,(key,))

    #update request with tech side info
    for record in request:
        query = ("UPDATE requests SET tech_name=?, urgency=?, status=?")
        c.execute(query,(tech,urgency,status,))
        db.commit()
        db.close()
        return "Request accepted!"

    #return error message if request entry doesn't exist
    return "Request doesn't exist."

#------------------------------------------------------
# Get ticket with given primary_key, return dictionary
#------------------------------------------------------
def get_request(key):
    db = connect(f)
    c = db.cursor()

    #find request with given primary key
    query = ("SELECT * FROM requests WHERE primary_key=?")
    request = c.execute(query,(key,))

    #create dictionary with request information
    request_info = {}
    for record in request:
        request_info['teacher_name'] = record[1]
        request_info['date_of_request'] = record[2]
        request_info['room_num'] = record[3]
        
