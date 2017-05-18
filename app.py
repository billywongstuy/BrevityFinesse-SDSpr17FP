from flask import Flask, render_template, request, session, redirect, url_for
from utils import auth, request_manager as reqs
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
        return render_template('index.html')
    #level 0 = superadmin
    elif session['level'] == 0:
        return 'superadmin<br><a href=\"logout\">Logout</a>'
    #level 1 = admin
    elif session['level'] == 1:
        return 'admin<br><a href=\"logout\">Logout</a>'
    #level 2 = tech
    elif session['level'] == 2:
        return 'tech<br><a href=\"logout\">Logout</a>'
    #level 3 = teacher/guest
    elif session['level'] == 3:
        return 'teacher<br><a href=\"logout\">Logout</a>'
    else:
        return 'You broke the page!'
    
@app.route("/ticket/<tid>")
def ticket(tid):
    return tid

#-----------------
# LOGINS
#-----------------

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
        session['type'] = auth.account_type(username)  #get account type
        return redirect('/')

    return loginMessage   #return error message for invalid login

@app.route("/logout", methods=['GET','POST'])
def logout():
    session.pop('username')
    session.pop('type')
    return redirect('/')
#nder_template('index.html')


#-------------------------
# TEACHER FUNCTIONS
#-------------------------

guest_allow = True

@app.route("/submit", methods=['POST','GET'])
def submit():
    if request.method == 'GET':
        return render_template("submit.html", isLogged=('username' in session))
    subj = request.form['subject']
    desc = request.form['desc']
    room = int(request.form['room'])
    hour = int(strftime("%H",gmtime()))-4
    date = strftime("%Y-%m-%d a:%M:%S", gmtime())
    date.replace('a',str(hour))
    
    if 'username' not in session:
        name = request.form['name']
    else:
        name = session['username']
        
    reqs.add_request(name,date,room,subj,body)
    
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

@app.route("/old_ticketts_tech", methods=['POST','GET'])
def old_tickets_tech():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

#--------------------------
# ADMIN FUNCTIONS
#--------------------------

admin_access = ['admin','superadmin']

@app.route("/all_tickets", methods=['POST','GET'])
def all_tickets():
    if not 'username' in session or not session['type'] in admin_access:
        return redirect('/')
    return

@app.route("/create_account", methods=['POST','GET'])
def create_account():
    if not 'username' in session or not session['type'] in admin_access:
        return redirect('/')
    return render_template('register.html')

@app.route("/guest_toggle", methods=['POST','GET'])
def guest_toggle():
    if not 'username' in session or not session['type'] in admin_access:
        return redirect('/')
    return

#-------------------------
# SUPERADMIN FUNCTIONS
#-------------------------

@app.route("/admin_promote", methods=['POST','GET'])
def admin_promote():
    if not 'username' in session or session['type'] != 'superadmin' :
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
