from flask import Flask, render_template, request, session, redirect, url_for
from utils import auth, tickets_manager as tix, email_handler as e_mail, archive
import calendar, datetime, json, os
from time import gmtime,strftime,mktime,strptime,sleep

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


app = Flask(__name__)
app.secret_key = os.urandom(32)
now = datetime.datetime.now()

statuses = {0:'Pending', 1:'Resolved', 2:'Coming At', 3: 'Deferred to'}

#---------------------------
# ROOT (INDEX)
#---------------------------

@app.route("/", methods=['POST','GET'])
def home():

    if 'username' not in session:
        return render_template('index.html')

    guest_allow = (auth.get_level('guest') == 4)
    lvl = session['level'] if 'username' in session else 4
    
    if session['level'] == 0: #superadmin
        return render_template('superadmin-dashboard.html', guest_allow=guest_allow) #DASHBOARD
    
    elif session['level'] == 1: #admin
        return render_template('admin-dashboard.html', guest_allow=guest_allow)

    elif session['level'] == 2: #tech
        pending = tix.all_tickets_with(0)
        done = tix.all_tickets_with(1)
        progress = tix.all_tickets_with(2)
        return render_template('tickets-all.html',pending=pending,progress=progress,done=done,loggedIn=True,level=lvl)
        #return render_template('index-tech.html',pending=pending,progress=progress,done=done)

    elif session['level'] == 3: #teacher
        pending = tix.all_tickets_from(session['username'],0)
        progress = tix.all_tickets_from(session['username'],2)
        done = tix.all_tickets_from(session['username'],1)
        return render_template('tickets-all.html',pending=pending,progress=progress,done=done,loggedIn=True,level=lvl)
        #return render_template('index-teacher.html',pending=pending,progress=progress,done=done,loggedIn=True)

    else:
        return 'You broke the page!!!'
    
#-----------------
# LOGIN / LOGOUT
#-----------------

@app.route("/login/", methods=['POST','GET'])
@app.route("/login", methods=['POST','GET'])
def login():
    #redirect in logged in
    if 'username' in session:
        return redirect('/')
    
    #render login page
    if request.method == 'GET':
        return render_template('login.html',message='')
    
    #validate login
    username = request.form['user']
    password = request.form['pass']
    loginMessage = auth.login(username,password)

    if username == 'guest':
        return render_template('login.html',message='Username does not exist')
    
    #loginMessage = "" if login is valid --> go to index page
    if loginMessage == "":
        session['username'] = username    #session username
        session['level'] = int(auth.account_level(username))  #get account type
        return redirect('/')

    return render_template('login.html',message=loginMessage)   #return error message for invalid login

@app.route("/logout", methods=['GET','POST'])
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('level')
    return redirect('/') 

#------------------------------------------------
# TICKET CREATION
#------------------------------------------------


# need email funcion for the guests
# auto fill with teacher email if logged in
# make email field show for guests and admins
# turn off create tickets for techs

@app.route("/submit", methods=['POST','GET'])
def submit():
    guest_allow = (auth.get_level('guest') == 4)
    
    if 'username' not in session and not guest_allow:
        return 'no' #render_template('guestunavail.html')
    
    if request.method == 'GET':
        return render_template("submit.html", teacherAcc=('username' in session and session['level'] == 3), loggedIn = 'username' in session)
    
    room = int(request.form['room'])
    if room <= 100 or room >= 1050:
        return render_template('submit.html', loggedIn=('username' in session), error='Invalid room number')
    
    subj = int(request.form['subject'])
    desc = request.form['desc']
    date = str(datetime.datetime.now())
    date = date[0:date.find('.')]
    
    if 'username' not in session or session['level'] != 3:
        u_name = 'guest'
        l_name = request.form['guestLastName']
        f_name = request.form['guestFirstName']
        t_name = l_name + ', ' + f_name
        email = request.form['email']
    else:
        u_name = session['username']
        t_name = auth.get_name(u_name)

        if session['level'] == 2: # techs+
            email = request.form['email']
        else:
            email = auth.get_email(session['username'])
        
    key = tix.add_ticket(u_name,t_name,date,room,subj,desc,email)

    subj = 'Ticket submitted'
    body = 'New ticket submitted'

    #cc fails tyr in future to send to self and cc to techs
    e_mail.send_msg_multi(auth.get_tech_emails(),subj,body)
    return redirect("/ticket/%d" % (int(key)))
    
#-------------------------
# TICKET VIEWING
#-------------------------

@app.route('/guest_tickets', methods=['GET','POST'])
def guest_tickets():
    #get all the guest tickets
    pending = tix.all_tickets_from('guest',0)
    progress = tix.all_tickets_from('guest',2)
    done = tix.all_tickets_from('guest',1)   
    return render_template('tickets-guest.html',pending=pending,progress=progress,done=done)


@app.route("/all_tickets", methods=['POST','GET'])
def all_tickets():

    if 'username' not in session:
        pending = tix.all_tickets_from('guest',0)
        progress = tix.all_tickets_from('guest',2)
        done = tix.all_tickets_from('guest',1)
    elif session['level'] == 3:
        pending = tix.all_tickets_from(session['username'],0)
        progress = tix.all_tickets_from(session['username'],2)
        done = tix.all_tickets_from(session['username'],1)
    elif session['level'] <= 2:
        pending = tix.all_tickets_with(0)
        progress = tix.all_tickets_with(2)
        done = tix.all_tickets_with(1)
    else:
        return 'Error?'

    lvl = session['level'] if 'username' in session else 4
    
    return render_template('tickets-all.html',pending=pending,progress=progress,done=done,loggedIn='username' in session,level=lvl)

#-----------------------------
# INDIVIDUAL TICKET PAGES
#-----------------------------

tixUpdateMsg = ""

@app.route("/ticket/<tid>", methods=["GET","POST"])
def ticket(tid):
    global tixUpdateMsg
    
    if request.method == 'GET':
        info = tix.get_ticket(tid)
        if info == 'Ticket doesn\'t exist':
            return 'Ticket doesn\'t exist'
        
        ta = 'username' in session and session['level'] <= 2
        aa = 'username' in session and session['level'] <= 1
        loggedIn = 'username' in session
        msg = str(tixUpdateMsg)
        tixUpdateMsg = ""

        if ta and info['when'] != None:
            info['when'] = info['when'].replace(' ','T')
            
        return render_template('ticket.html',techAccess=ta,info=info,message=msg, loggedIn=loggedIn, adminAccess=aa) 


    if request.method == 'POST' and 'username' not in session:
        return redirect("/.")
    
    # changing a ticket
    if session['level'] > 1: #tech
        tech = auth.get_name(session['username'])
    else: #admin
        tech = request.form['tech']
     
    status = int(request.form['status'])
    urgency = int(request.form['urgency'])

    if status >= 2:
        w = request.form['when'] 
        pattern = '%Y-%m-%dT%H:%M'
        when = int(mktime(strptime(w,pattern))) #epoch conversion
    else:
        when = None

    tix.update_ticket(tid,tech,urgency,status,when) # update the ticket

    # SENDING EMAIL
    t_name = tix.get_name(int(tid))
    t_name = t_name[(t_name.find(',')+2):] + ' ' + t_name[:t_name.find(',')]
    full_status = str(statuses[status]) if when == None else str(statuses[status] + ' ' + w.replace('T',' '))
    urge = tix.get_urgency(int(tid))
    
    t_email = tix.get_email(int(tid))
    subj = 'StuyTix: Ticket #%d Status Changed' % (int(tid))
    body = e_mail.get_update_body(t_name, full_status,urge)

    e_mail.send_msg_one(t_email,subj,body)
    
    tixUpdateMsg = 'Ticket updated!'
    
    return redirect('/ticket_reload/%d' % (int(tid)))

#-----------------------
# TICKET RELOAD PASS
#------------------------

@app.route('/ticket_reload/<tid>', methods=['GET'])
def ticket_reload(tid):
    return redirect('/ticket/%d' % (int(tid)))

#--------------------------
# ADMIN FUNCTIONS
#--------------------------

admin_access = [0,1]

@app.route("/create_account", methods=['POST','GET'])
def create_account():
    if not 'username' in session or not session['level'] in admin_access:
        return redirect('/')    
    if request.method == 'GET':
        return render_template('register.html',message=None,isSuper=session['level'] == 0)
    
    user = request.form['user']
    email = request.form['email']
    email2 = request.form['emailconf']
    if email != email2:
        return render_template('register.html',message='Unmatching emails!')
    
    passw = request.form['pass']
    pass2 = request.form['passconf']
    account = request.form['account']
    phone = request.form['phone']
    f_name = request.form['firstName']
    l_name = request.form['lastName']
    msg = auth.register(user,l_name,f_name,email,passw,pass2,account,phone)

    return render_template('register.html',message=msg,isSuper=session['level']==0)


@app.route("/guest_toggle", methods=['POST'])
def guest_toggle():
    guest_allow = (auth.get_level('guest') == 4)
    choice = str(request.form['guest_choices'])
    if choice == 'on' and not guest_allow:
        auth.guest_on()
    elif choice == 'off' and guest_allow:
        auth.guest_off()
        
    return redirect('/')

#-------------------------
# SUPERADMIN FUNCTIONS
#-------------------------

@app.route("/admin_promote", methods=['POST','GET'])
def admin_promote():
    if not 'username' in session or session['level'] != 0:
        return redirect('/')

    if request.method == 'GET':
        return render_template('promote.html')
    
    #u_name = request.form['username']
    #action = request.form['action']

    #need this functions to be written
    #if action == 'promote':
    #promote     (takes in username and new rank)
    #elif action == 'demote':
    #revoke/demote    (takes in username and new rank)
    return render_template('promote.html')

#------------------
# ERROR HANDLERS
#------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


#---------------------------
# SCHEDULED DAILY ARCHIVE
#--------------------------

def archive_do():
    return archive.create_csv(str(now.date()))
    
sched = BackgroundScheduler()
sched.add_job(archive_do,'cron',hour=17,minute=0,second=0)
sched.start()

#--------------
# Start
#-------------

def start_flask():
    app.run(debug=True, use_reloader=True) #Set debug to False before publishing

if __name__ == "__main__":
    start_flask()
