from sqlite3 import connect
from hashlib import sha1
from os import urandom
import random,string,time

f = "data/tix.db"

statuses = {0:'Pending', 1:'Resolved', 2:'Coming at', 3: 'Deferred to'}
time_pattern = '%Y-%m-%dT%H:%M'

issues = {
    0: 'Out of Toner',
    1: 'Printer Issues (paper jam, does not print, printer error, etc)',
    2: 'Laptop Issues',
    3: 'Smartboard/Projector Issues(screen, display, volume, etc)',
    4: 'Need item/equipment (please describe)',
    5: 'Other (please describe)'
}

#-----------------------------
# Teacher create request
#-----------------------------
def add_ticket(username,teacher,date,room,subject,body=None):
    db = connect(f)
    c = db.cursor()
    #select table tickets, create table tickets if doesn't exist
    try:
        c.execute("SELECT * FROM tickets")
    except:
        c.execute("CREATE TABLE tickets (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, teacher_name TEXT, date_of_ticket TEXT, room_num INT, tix_subject INTEGER, tix_body TEXT, tech_name TEXT, urgency INT, status INT, resp_time INT)")

    #create ticket entry with given info
    query = ("INSERT INTO tickets (username,teacher_name,date_of_ticket,room_num,tix_subject,tix_body,status,resp_time) VALUES (?,?,?,?,?,?,?,?)")
    c.execute(query,(username,teacher,date,room,subject,body,0,None,))
    db.commit()
    db.close()
    return c.lastrowid

#------------------------------
# Tech accepts/updates ticket
#------------------------------
def update_ticket(key,tech,urgency,status,when):
    db = connect(f)
    c = db.cursor()
    query = ("UPDATE tickets SET tech_name=?, urgency=?, status=?, resp_time=? WHERE primary_key=?")
    c.execute(query,(tech,urgency,status,when,key,))
    db.commit()
    db.close()
    return "Ticket accepted!"


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
        ticket_info['primary_key'] = record[0]
        ticket_info['username'] = record[1]
        ticket_info['teacher_name'] = record[2]
        ticket_info['date_of_ticket'] = record[3]
        ticket_info['room_num'] = record[4]
        ticket_info['tix_subject'] = issues[record[5]]
        ticket_info['tix_body'] = record[6]
        ticket_info['tech_name'] = record[7]
        ticket_info['urgency'] = record[8]
        ticket_info['status'] = statuses[record[9]]
        ticket_info['when'] = None
        
        if record[9] >= 2:
            until = time.strftime(time_pattern, time.localtime(record[10]))
            ticket_info['when'] = str(until)
            
        db.commit()
        db.close()
        return ticket_info
    db.commit()
    db.close()
    return "Ticket doesn't exist"

#----------------------------------
# Get ALL tickets
#---------------------------------
def all_tickets():
    db = connect(f)
    c = db.cursor()

    #find all tickets
    query = ("SELECT * FROM tickets")
    tickets = c.execute(query)

    #create list of dictionaries with ticket info
    ticket_list = []
    for record in tickets:
        ticket_info = {}
        ticket_info['primary_key'] = record[0]
        ticket_info['username'] = record[1]
        ticket_info['teacher_name'] = record[2]
        ticket_info['date_of_ticket'] = record[3]
        ticket_info['room_num'] = record[4]
        ticket_info['tix_subject'] = issues[record[5]]
        ticket_info['tix_body'] = record[6]
        ticket_info['tech_name'] = record[7]
        ticket_info['urgency'] = record[8]
        ticket_info['status'] = statuses[record[9]]
        ticket_info['when'] = None
        
        if record[9] >= 2:
            until = time.strftime(time_pattern, time.localtime(record[10]))
            ticket_info['when'] = str(until)
        
        ticket_list.append(ticket_info)
    return ticket_list


#------------------------------------------------------------
# Get tickets of given status,return list of dictionaries
# 0:pending; 1: resolved, 2+: in progress 
#------------------------------------------------------------
def all_tickets_with(status):
    db = connect(f)
    c = db.cursor()

    #find all tickets with given status

    if status == 2:
        query = ("SELECT * FROM tickets WHERE status >= 2")
        tickets = c.execute(query)
    else:
        query = ("SELECT * FROM tickets WHERE status=?")
        tickets = c.execute(query,(status,))

    #create list of dictionaries with ticket info
    ticket_list = []
    for record in tickets:
        ticket_info = {}
        ticket_info['primary_key'] = record[0]
        ticket_info['username'] = record[1]
        ticket_info['teacher_name'] = record[2]
        ticket_info['date_of_ticket'] = record[3]
        ticket_info['room_num'] = record[4]
        ticket_info['tix_subject'] = issues[record[5]]
        ticket_info['tix_body'] = record[6]
        ticket_info['tech_name'] = record[7]
        ticket_info['urgency'] = record[8]
        ticket_info['status'] = statuses[record[9]]
        ticket_info['when'] = None
        
        if record[9] >= 2:
            until = time.strftime(time_pattern, time.localtime(record[10]))
            ticket_info['when'] = str(until)
            
        ticket_list.append(ticket_info)
    return ticket_list


#-----------------------------------------------------------------------------
# Get tickets of given status from given username,return list of dictionaries
# 0: pending, 1: resolved, 2+: in progress
#-----------------------------------------------------------------------------
def all_tickets_from(username,status):
    db = connect(f)
    c = db.cursor()
    
    #find all tickets with given status from given username

    if status == 2:
        query = ("SELECT * FROM tickets WHERE username=? AND status >= 2")
        tickets = c.execute(query,(username,))
    else:
        query = ("SELECT * FROM tickets WHERE username=? AND status=?")
        tickets = c.execute(query,(username,status,))

    #create list of dictionaries with ticket info
    ticket_list = []
    for record in tickets:
        ticket_info = {}
        ticket_info['primary_key'] = record[0]
        ticket_info['username'] = record[1]
        ticket_info['teacher_name'] = record[2]
        ticket_info['date_of_ticket'] = record[3]
        ticket_info['room_num'] = record[4]
        ticket_info['tix_subject'] = issues[record[5]]
        ticket_info['tix_body'] = record[6]
        ticket_info['tech_name'] = record[7]
        ticket_info['urgency'] = record[8]
        ticket_info['status'] = statuses[record[9]]
        ticket_info['when'] = None
        
        if record[9] >= 2:
            until = time.strftime(time_pattern, time.localtime(record[10]))
            ticket_info['when'] = str(until)
            
        ticket_list.append(ticket_info)
    return ticket_list
    

#------------------------
# Tech closes ticket
#------------------------
def close_ticket(key):
    db = connect(f)
    c = db.cursor()
    #change status of ticket
    query = ("UPDATE tickets SET status=? WHERE primary_key=?")
    c.execute(query,(2,key,))
    db.commit()
    db.close()
    return "Ticket closed!"

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
drop()
print add_ticket("guest","teacher2","05/17/17","110","electronic")
print add_ticket("guest","teacher2","05/17/17","111","electronic")
print add_ticket("guest","teacher2","05/17/17","112","electronic")
print add_ticket("user1","teacher1","05/17/17","113","electronic")
print accept_ticket(1,"tech2","4")
print all_tickets_with(0)
print
print all_tickets_from("user1",1)
print
print all_tickets()

'''
