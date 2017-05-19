from sqlite3 import connect
from hashlib import sha1
from os import urandom
import random,string

f = "data/tix.db"


#-------------------------
# Login
#-------------------------
def login(username, password):
    db = connect(f)
    c = db.cursor()

    #select table users, create table users if doesn't exist
    try:
        c.execute("SELECT * FROM USERS")
    except:
        c.execute("CREATE TABLE users (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, salt TEXT, type TEXT, phone_num TEXT)")

    #find account with given username
    query = ("SELECT * FROM users WHERE username=?")
    info = c.execute(query,(username,))

    #check password
    for record in info:
        password = sha1(password+record[4]).hexdigest() #record[4] is the salt
        if (password==record[3]): #record[3] is password
            return ""#login success,no error message
        else:
            return "User login has failed. Invalid password"#error message
        db.commit()
        db.close()
        
    return "Username does not exist"#error message

#---------------------
# Get account type
#---------------------
def account_type(username):
    db = connect(f)
    c = db.cursor()

    #find account with given username
    query = ("SELECT * FROM users WHERE username=?")
    account = c.execute(query,(username,))

    #return account type
    for record in account:
        return record[5] #record[5] is type

#------------------------
# NOT IN USE
#------------------------
def getSize():
    db = connect(f)
    c = db.cursor()
    num = c.execute("SELECT COUNT(*) FROM USERS")
    size = 0
    for record in num:
        size = record[0]
    db.commit()
    db.close()
    return size

#----------------------
# Register
#---------------------
def register(username,email,password,pw2,account_type,phone_num):

    #confirm password
    if password != pw2:
        return "Passwords not the same."

    #check whether username exists already
    if duplicate(username):
        return "Username already exists"
    
    db = connect(f, timeout=10)
    c = db.cursor()
    
    #select table users, create table users if doesn't exist
    try:
        c.execute("SELECT * FROM USERS")
        print ("table exist")
    except:
        c.execute("CREATE TABLE users (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT, salt TEXT, type TEXT, phone_num TEXT)")

    #check if email is valid, reg = "" if valid
    reg = errorMsg(email, password)
    if reg == "":
        #Create account with given info
        salt = urandom(10).encode('hex')
        query = ("INSERT INTO users (username,email,password,salt,type,phone_num) VALUES (?, ?, ?, ?, ?, ?)")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (username, email, password, salt, account_type, phone_num))
        c.execute('SELECT * from users')
        db.commit()
        db.close()
        return "Account created!"

    #Return error message for invalid email
    db.commit()
    db.close()
    return reg

#-------------------------------
# Validate email address
#-------------------------------
def errorMsg(email, password):      
    if '@' not in email:
        return "Please enter a valid email."
    if duplicate(email):
        return "User account already exists"
    if " " in email or " " in password:
        return "Spaces not allowed in email or password"
    if len(password) <= 8:
        return "Passwords must be at least 8 characters"
    return ""

#------------------------------
# Change password
#------------------------------
def changepwd(username,old,new,new2):
    #error messages for invalid new password
    if new != new2:
        return "New passwords are not identical"
    if len(new) < 8:
        return "Passwords must be greater than 8 characters"
    if old == new:
        return "Old and new passwords are the same"

    db = connect(f)
    c = db.cursor()

    #find account with given username
    query = ("SELECT * FROM users WHERE username=?")
    account = c.execute(query, (username,))
    for record in account:
        #validate old password
        oldP = sha1(old+record[4]).hexdigest() #record[4] is the salt
        if record[3] == oldP:#record[3] is password
            #old password is correct, change to new password
            salt = urandom(10).encode('hex')
            password = sha1(new + salt).hexdigest()
            query = ("UPDATE users SET password=?, salt=? WHERE username=?")
            c.execute(query, (password,salt,username))
            db.commit()
            db.close()
            return "Password successfully changed"
        #error message for incorrect old password
        return "Incorrect old password"
    return "unexpected error"

#-------------------------------------
# Checks if username already exists
#-------------------------------------
def duplicate(username):
    db = connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE username=?")
    sel = c.execute(query, (username,))
    value = False
    for record in sel:
        value = True
    db.commit()
    db.close()
    return value

#--------------------------
# Change account level
#-------------------------
def change_level(key):
    db = connect(f)

#-------------------------------
# NOT IN USE AT THE MOMENT
#-------------------------------
def admin_resetpwd(email):
    db = connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE username=?")
    sel = c.execute(query, (email,))
    for record in sel:

        new = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        salt = urandom(10).encode('hex')
        password = sha1(new + salt).hexdigest()
        
        
        query = ("UPDATE users SET password=?, salt=? WHERE email=?")
        c.execute(query, (password,salt,email))
        db.commit()
        db.close()

        return new
    
    return "Email does not exist in database!"


#----------------------------
# Drop table users(debug)
#---------------------------
def drop()
    db = connect(f)
    c = db.cursor()

    c.execute("DROP TABLE users")
    db.commit()
    db.close()
    return "users db dropped"
