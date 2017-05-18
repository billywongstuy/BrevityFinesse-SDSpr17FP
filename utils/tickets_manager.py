from sqlite3 import connect
from hashlib import sha1
from os import urandom
import random,string

f = "data/tix.db"

#-----------------------------
# Teacher create request
#-----------------------------
def add_ticket(teacher,date,room,subject,body=None):
    db = connect(f)
    c = db.cursor()
    #select table tickets, create table tickets if doesn't exist
    try:
        c.execute("SELECT * FROM tickets")
    except:
        c.execute("CREATE TABLE tickets (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, teacher_name TEXT, date_of_ticket TEXT, room_num INT, tix_subject TEXT, tix_body TEXT, tech_name TEXT, urgency INT, status INT)")

    #create ticket entry with given info
    query = ("INSERT INTO tickets (teacher_name,date_of_ticket,room_num,tix_subject,tix_body,status) VALUES (?,?,?,?,?,?)")
    c.execute(query,(teacher,date,room,subject,body,0,))
    db.commit()
    db.close()
    return "Ticket created!"

#---------------------------
# Tech accepts ticket
#---------------------------
def accept_ticket(key,tech,urgency):
    db = connect(f)
    c = db.cursor()

    #find ticket with given primary key
    query = ("SELECT * FROM tickets WHERE primary_key=?")
    ticket = c.execute(query,(key,))

    #update ticket with tech side info
    for record in ticket:
        query = ("UPDATE tickets SET tech_name=?, urgency=?, status=?")
        c.execute(query,(tech,urgency,1,))
        db.commit()
        db.close()
        return "Ticket accepted!"

    #return error message if ticket entry doesn't exist
    return "Ticket doesn't exist."

#------------------------------------------------------
# Get ticket with given primary_key, return dictionary
#------------------------------------------------------
def get_ticket(key):
    db = connect(f)
    c = db.cursor()

    #find ticket with given primary key
    query = ("SELECT * FROM tickets WHERE primary_key=?")
    ticket = c.execute(query,(key,))

    #create dictionary with ticket information
    ticket_info = {}
    for record in ticket:
        ticket_info['teacher_name'] = record[1]
        ticket_info['date_of_ticket'] = record[2]
        ticket_info['room_num'] = record[3]
        ticket_info['tix_subject'] = record[4]
        ticket_info['tix_body'] = record[5]
        ticket_info['tech_name'] = record[6]
        ticket_info['urgency'] = record[7]
        ticket_info['status'] = record[8]
        db.commit()
        db.close()
        return ticket_info
    db.commit()
    db.close()
    return "Ticket doesn't exist"

#------------------------
# Tech closes ticket
#------------------------
def close_ticket(key):
    db = connect(f)
    c = db.cursor()

    #find ticket with given key
    query = ("SELECT * FROM tickets WHERE primary_key=?")
    ticket = c.execute(query,(key,))

    #change status of ticket
    for record in ticket:
        query = ("UPDATE tickets SET status=?")
        c.execute(query,(2,))
        db.commit()
        db.close()
        return "Ticket closed!"
    return "Ticket doesn't exist"


#----------------------
# Drop table(debug use)
#----------------------
def drop():
    db = connect(f)
    c = db.cursor()
    c.execute("DROP TABLE tickets")
    db.commit()
    db.close()
    return "Table tickets dropped"

#--------------------
# Testing area
#--------------------
'''
print drop()
print add_ticket("teacher2","05/17/17","110","electronic")
print get_ticket(1)
print accept_ticket(1,"tech2","4")
print get_ticket(1)
print close_ticket(1)
print get_ticket(1)
'''
