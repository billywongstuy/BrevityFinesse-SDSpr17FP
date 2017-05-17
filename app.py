from flask import Flask, render_template, request, session, redirect, url_for
from utils import auth
import calendar, datetime, json, os

app = Flask(__name__)
app.secret_key = os.urandom(32)

#---------------------------
# ROOT AND GUEST FUNCTION
#---------------------------

@app.route("/", methods=['POST','GET'])
def home():
    if 'user' not in session:
        return render_template('index.html')
    elif session['type'] == 'teacher':
        return
    elif session['type'] == 'tech':
        return
    elif session['type'] == 'admin':
        return
    elif session['type'] == 'superadmin':
        return
    else:
        return 'You broke the page!'
    


#-----------------
# LOGINS
#-----------------

@app.route("/super_login", methods=['POST','GET'])
def superadmin_login():
    if method == 'GET':
        return #render_template
    user = request.form['user']
    pw = request.form['pw']
    login_ok = auth.login(user,pw)
    if login_ok == '':
        session['user'] = user
        session['type'] = 'superadmin'
        return redirect('/')
    return #render_template

@app.route("/login", methods=['POST','GET'])
def login():
    #render login page
    if request.method == 'GET':
        return render_template('login.html')

    #validate login
    username = request.form["user"]
    password = request.form["pass"]
    loginMessage = auth.login(username,password)
    
    #loginMessage = "" if login is valid --> go to index page
    if loginMessage == "":
        return redirect("/")

    #return error message for invalid login
    return loginMessage


#-------------------------
# TEACHER FUNCTIONS
#-------------------------

@app.route("/make_request", methods=['POST','GET'])
def make_request():
    if not 'username' in session:
        return redirect("/")
    return

@app.route("/pending_requests_teacher", methods=['POST','GET'])
def pending_requests_teacher():
    if not 'username' in session:
        return redirect("/")
    return

@app.route("/old_requests_teacher", methods=['POST','GET'])
def old_requests_teacher():
    if not 'username' in session:
        return redirect("/")
    return


#-------------------------
# TECH FUNCTIONS
#-------------------------

@app.route("/new_requests", methods=['POST','GET'])
def new_requests():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

@app.route("/pending_requests_tech", methods=['POST','GET'])
def pending_requests_tech():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

@app.route("/old_requests_tech", methods=['POST','GET'])
def old_requests_tech():
    if not 'username' in session or session['type'] != 'tech':
        return redirect("/")
    return

#--------------------------
# ADMIN FUNCTIONS
#--------------------------

admin_access = ['admin','superadmin']

@app.route("/all_requests", methods=['POST','GET'])
def all_requests():
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
    return 'Page not found'


#--------------
# Start
#-------------
if __name__ == "__main__":
    app.debug = True
    app.run()