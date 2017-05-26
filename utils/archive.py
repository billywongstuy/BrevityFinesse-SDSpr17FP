import csv
from sqlite3 import connect

f = "data/tix.db"

#----------------------------
# Status chart
#----------------------------
statuses = {0:'Pending',
            1:'Resolved',
            2:'Coming at',
            3: 'Deferred to'}

#------------------------
# ticket category chart
#------------------------
issues = {
    0: 'Out of Toner',
    1: 'Printer Issues (paper jam, does not print, printer error, etc)',
    2: 'Laptop Issues',
    3: 'Smartboard/Projector Issues(screen, display, volume, etc)',
    4: 'Need item/equipment (please describe)',
    5: 'Other (please describe)'
}

#-----------------------
# ticket urgency chart
#-----------------------
urgency = {
    0 : 'Low',
    1 : 'Medium',
    2 : 'High',
    None : ''
    }

#--------------------------------------------------
#Create archive CSV file, named with given date
#--------------------------------------------------
def create_csv(date):
    with open('data/' + date + '.csv','w') as csvfile:

        #create headers
        fieldnames = ['ID','teacher_username','teacher_name','submission_time','room_number','issue','description','tech_name','urgency','status','respond_time','teacher_email']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        db = connect(f)
        c = db.cursor()
        
        #add resolved tickets, removed from tickets database
        query = ("SELECT * FROM tickets WHERE status=?")
        resolved_tickets = c.execute(query,(1,))
        for record in resolved_tickets:
            writer.writerow({'ID':record[0],
                             'teacher_username':record[1],
                             'teacher_name':record[3],
                             'submission_time':record[3],
                             'room_number':record[4],
                             'issue':issues[record[5]],
                             'description':record[6],
                             'tech_name':record[7],
                             'urgency':urgency[record[8]],
                             'status':statuses[record[9]],
                             'respond_time':record[10],
                             'teacher_email':record[11]})
        c.execute("DELETE FROM tickets WHERE status=?",(1,))

        #add other tickets
        query = ("SELECT * FROM tickets")
        other_tickets = c.execute(query)
        for record in other_tickets:
            writer.writerow({'ID':record[0],
                             'teacher_username':record[1],
                             'teacher_name':record[3],
                             'submission_time':record[3],
                             'room_number':record[4],
                             'issue':issues[record[5]],
                             'description':record[6],
                             'tech_name':record[7],
                             'urgency':urgency[record[8]],
                             'status':statuses[record[9]],
                             'respond_time':record[10],
                             'teacher_email':record[11]})
        db.commit()
        db.close()
        return "Archive created."

#create_csv("2017-05-25")
