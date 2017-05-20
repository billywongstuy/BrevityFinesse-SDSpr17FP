from flask import Flask, render_template, request, session, redirect, url_for
from utils import auth, tickets_manager as tix
import calendar, datetime, json, os
from time import gmtime,strftime

app = Flask(__name__)
app.secret_key = os.urandom(32)

'''
Statuses

Pending
In Progress
    - Will Come Today At
    - Deferred Until
Done
'''

statuses = {0:'Pending', 1:'Resolved', 2:'Coming At', 3: 'Deferred to'}

#---------------------------
# ROOT (INDEX)
#---------------------------

@app.route("/", methods=['POST','GET'])
def home():
    if 'username' not in session:
        return render_template('index.html')
    
    if session['level'] == 0: #superadmin
        return render_template('superadmin-dashboard.html')#'superadmin<br><a href=\"logout\">Logout</a>' #DASHBOARD
    
    elif session['level'] == 1: #admin
        return render_template('admin-dashboard.html')

    elif session['level'] == 2: #tech
        pending = tix.all_tickets_with(0)
        done = tix.all_tickets_with(1)
        progress = tix.all_tickets_with(2)
        return render_template('index-tech.html',pending=pending,progress=progress,done=done)

    elif session['level'] == 3: #teacher
        pending = tix.all_tickets_from(session['username'],0)
        progress = tix.all_tickets_from(session['username'],2)
        done = tix.all_tickets_from(session['username'],1)
        return render_template('index-teacher.html',pending=pending,progress=progress,done=done)

    else:
        return 'You broke the page!'

#-----------------
# LOGIN / LOGOUT
#-----------------

@app.route("/login/", methods=['POST','GET'])
@app.route("/login", methods=['POST','GET'])
def login():
    #render login page
    if request.method == 'GET':
        return render_template('login.html')

    #validate login
    username = request.form['user']
    password = request.form['pass']
    loginMessage = auth.login(username,password)
    
    #loginMessage = "" if login is valid --> go to index page
    if loginMessage == "":
        session['username'] = username    #session username
        session['level'] = int(auth.account_level(username))  #get account type
        return redirect('/')

    return loginMessage   #return error message for invalid login

@app.route("/logout", methods=['GET','POST'])
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('level')
    return redirect('/') #render_template('index.html')

#------------------------------------------------
# TICKET CREATION
#------------------------------------------------


@app.route("/submit", methods=['POST','GET'])
def submit():
    guest_allow = (auth.get_level('guest') == 4)
    
    if 'username' not in session and not guest_allow:
        return 'no' #render_template('guestunavail.html')
    
    if request.method == 'GET':
        return render_template("submit.html", teacherAcc=('username' in session and session['level'] == 3))
    
    room = int(request.form['room'])
    if room <= 100 or room >= 1050:
        return render_template('submit.html', isLogged=('username' in session), error='Invalid room number')
    
    subj = request.form['subject']
    desc = request.form['desc']
    date = str(datetime.datetime.now())
    date = date[0:date.find('.')]
    
    if 'username' not in session:
        u_name = 'guest'
        l_name = request.form['guestLastName']
        f_name = request.form['guestFirstName']
        t_name = l_name + ', ' + f_name
    else:
        u_name = session['username']
        t_name = auth.get_name(u_name)
        
    tix.add_ticket(u_name,t_name,date,room,subj,desc)
    return redirect("/")
    
#Functions to receive pending requests and old requests should be endpoints returning raw JSON data which will be displayed on a central profile page using JavaScript
#	- Julian


#-------------------------
# GUEST TICKET VIEWING
#-------------------------

@app.route('/guest_tickets', methods=['GET','POST'])
def guest_tickets():
    #get all the guest tickets
    pending = tix.all_tickets_from('guest',0)
    progress = tix.all_tickets_from('guest',2)
    done = tix.all_tickets_from('guest',1)
    
    return render_template('tickets-guest.html',pending=pending,progress=progress,done=done)


#-----------------------------
# INDIVIDUAL TICKET PAGES
#-----------------------------

@app.route("/ticket/<tid>")
def ticket(tid):
    info = get_ticket(tid)
    if request.method == 'GET':
        if info == 'Ticket doesn\'t exist':
            return 'Ticket doesn\'t exist'
        return render_template('ticket.html',techAccess=(session['level'] == 2),ticketInfo=info,message=None) #differentiates between being able to edit the ticket
    
    #tech = request.form['techName']  #auto-filled to tech name if present
    #status = request.form['status']
    #urgency = request.form['urgency']
    #time_until = request.form['timeUntil'] #convert this to epoch
    #time_until = epoch(time_until)
    
    # update the ticket
    #tix.accept_ticket(tid,tech,urgency,status,time_until)
    
    return render_template('ticket.html',techAccess=(session['level'] == 2),ticketInfo=info,message='Ticket updated!')



#--------------------------
# ADMIN FUNCTIONS
#--------------------------

admin_access = [0,1]

@app.route("/all_tickets", methods=['POST','GET'])
def all_tickets():
    if not 'username' in session or not session['level'] in admin_access:
        return redirect('/')
    pending = tix.all_tickets_with(0)
    progress = tix.all_tickets_with(2)
    done = tix.all_tickets_with(1)
    return render_template('tickets-all.html',pending=pending,progress=progress,done=done)

@app.route("/create_account", methods=['POST','GET'])
def create_account():
    if not 'username' in session or not session['level'] in admin_access:
        return redirect('/')
    
    if request.method == 'GET':
        return render_template('register.html',message=None)
    
    user = request.form['user']
    email = request.form['email']
    email2 = request.form['emailconf']
    
    if email != email2:
        return render_template('register.html')
    
    passw = request.form['pass']
    pass2 = request.form['passconf']
    account = request.form['account']
    phone = request.form['phone']
    f_name = request.form['firstName']
    l_name = request.form['lastName']
    
    msg = auth.register(user,l_name,f_name,email,passw,pass2,account,phone)

    return render_template('register.html',message=msg)

@app.route("/guest_toggle", methods=['POST'])
def guest_toggle():
    #do toggling stuff here
    return redirect('/')

#-------------------------
# SUPERADMIN FUNCTIONS
#-------------------------

@app.route("/admin_promote", methods=['POST','GET'])
def admin_promote():
    if not 'username' in session or session['level'] != 0:
        return redirect('/')

    return


#------------------
# ERROR HANDLERS
#------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


#--------------
# Start
#-------------
if __name__ == "__main__":
    app.debug = True  #Set to False before publishing
    app.run()
