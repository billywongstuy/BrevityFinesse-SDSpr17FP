from flask import Flask, render_template, request, session, redirect, url_for
from utils import auth, tickets_manager as tix
import calendar, datetime, json, os
from time import gmtime,strftime

app = Flask(__name__)
app.secret_key = os.urandom(32)

#---------------------------
# ROOT AND GUEST FUNCTION
#---------------------------

@app.route("/", methods=['POST','GET'])
def home():
    if 'username' not in session:
        #get all guest tickets
        return render_template('index.html')
    
    #when getting tickets, store in list of dictionaries
    elif session['type'] == 'superadmin': #['level'] == 0: #superadmin
        #get all unresponded tickets
        #get all pending tckets
        #get all done tickets
        return 'superadmin<br><a href=\"logout\">Logout</a>'
    elif session['type'] == 'admin': #['level'] == 1: #admin
        #get all unresponded tickets
        #get all pending tckets
        #get all done tickets
        return 'admin<br><a href=\"logout\">Logout</a>'
    elif session['type'] == 'tech': #['level'] == 2: #tech
        #get all unresponded tickets
        #get all pending tckets
        #get all done tickets
        return 'tech<br><a href=\"logout\">Logout</a>'
    elif session['type'] == 'teacher': #['level'] == 3: #teacher
        #get teach unresp tickets
        #get tech pending tickets
        #get teach done tickets
        return 'teacher<br><a href=\"logout\">Logout</a>'
    else:
        return 'You broke the page!'
    
@app.route("/ticket/<tid>")
def ticket(tid):
    #get all ticket info into a dictionary
    return tid

#-----------------
# LOGINS
#-----------------

@app.route("/login", methods=['POST','GET'])
@app.route("/login/", methods=['POST','GET'])
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
        session['type'] = auth.account_type(username)  #get account type
        return redirect('/')

    return loginMessage   #return error message for invalid login

@app.route("/logout", methods=['GET','POST'])
@app.route("/logout/", methods=['GET','POST'])
def logout():
    session.pop('username')
    session.pop('type')
    return redirect('/') #render_template('index.html')


#-------------------------
# GUEST TICKET VIEWING
#-------------------------

@app.route('/guest_tickets', methods=['GET','POST'])
def guest_tickets():
    #get all the guest tickets
    return 'guest tickets templates'


#------------------------------------------------
# TEACHER FUNCTIONS (EVERYONE INCLUDING GUEST)
#------------------------------------------------

guest_allow = True

@app.route("/submit", methods=['POST','GET'])
def submit():
    if request.method == 'GET':
        return render_template("submit.html", teacherAcc=('username' in session and session['type'] == 'teacher'))

    if 'username' not in session and not guest_allow:
        return render_template('guestunavail.html')
    
    room = int(request.form['room'])
    if room <= 100 or room >= 1050:
        return render_template('submit.html', isLogged=('username' in session), error='Invalid room number')
    
    subj = request.form['subject']
    desc = request.form['desc']
    date = str(datetime.datetime.now())
    date = date[0:date.find('.')]
    
    if 'username' not in session:
        name = request.form['guestName']
    else:
        name = session['username']

    tix.add_ticket(name,date,room,subj,desc)
    return redirect("/")
    
#Functions to receive pending requests and old requests should be endpoints returning raw JSON data which will be displayed on a central profile page using JavaScript
#	- Julian

# @app.route("/pending_requests_teacher", methods=['POST','GET'])
# def pending_requests_teacher():
#     if not 'username' in session:
#         return redirect("/")
#     return

# @app.route("/old_requests_teacher", methods=['POST','GET'])
# def old_requests_teacher():
#     if not 'username' in session:
#         return redirect("/")
#     return

def profile():
    if not 'username' in session:
        return redirect("/")
    return


#-------------------------
# TECH FUNCTIONS
#-------------------------

@app.route("/new_tickets", methods=['POST','GET'])
def new_tickets():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

@app.route("/pending_tickets_tech", methods=['POST','GET'])
def pending_tickets_tech():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

@app.route("/old_tickets_tech", methods=['POST','GET'])
def old_tickets_tech():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

#--------------------------
# ADMIN FUNCTIONS
#--------------------------

admin_access = ['admin','superadmin']

@app.route("/a", methods=['POST','GET'])
def all_tickets():
    if not 'username' in session or not session['type'] in admin_access:
        return redirect('/')
    return

@app.route("/create_account", methods=['POST','GET'])
def create_account():
    if not 'username' in session or not session['type'] in admin_access:
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
    
    msg = auth.register(user,email,passw,pass2,account,phone)

    return render_template('register.html',message=msg)
    
#-------------------------
# SUPERADMIN FUNCTIONS
#-------------------------

@app.route("/admin_promote", methods=['POST','GET'])
def admin_promote():
    if not 'username' in session or session['type'] != 'superadmin':
        return redirect('/')
    return

#------------------
# ERROR HANDLERS
#------------------

@app.errorhandler(404)
def page_not_found(e):
    #return render_template('404.html'), 404
    return render_template("404.html")


#--------------
# Start
#-------------
if __name__ == "__main__":
    app.debug = True  #Set to False before publishing
    app.run()
