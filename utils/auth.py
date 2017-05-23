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
        c.execute("CREATE TABLE users (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, last_name TEXT, first_name TEXT, email TEXT, password TEXT, salt TEXT, level TEXT, phone_num TEXT)")

    #find account with given username
    query = ("SELECT * FROM users WHERE username=?")
    info = c.execute(query,(username,))

    #check password
    for record in info:
        password = sha1(password+record[6]).hexdigest() #record[6] is the salt
        if (password==record[5]): #record[5] is password
            return ""#login success,no error message
        else:
            return "User login has failed. Invalid password"#error message
        db.commit()
        db.close()
        
    return "Username does not exist"#error message

#---------------------
# Get account level
#---------------------
def account_level(username):
    db = connect(f)
    c = db.cursor()

    #find account with given username
    query = ("SELECT * FROM users WHERE username=?")
    account = c.execute(query,(username,))

    #return account type
    for record in account:
        return record[7] #record[7] is level

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
def register(username,last,first,email,password,pw2,account_level,phone_num=None):
    db = connect(f, timeout=10)
    c = db.cursor()

    account_level = int(account_level)
    
    #select table users, create table users if doesn't exist
    try:
        c.execute("SELECT * FROM USERS")
    except:
        c.execute("CREATE TABLE users (primary_key INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, last_name TEXT, first_name TEXT, email TEXT, password TEXT, salt TEXT, level INTEGER, phone_num TEXT)")
        
    #confirm password
    if password != pw2:
        return "Passwords not the same."

    #check whether username exists already
    if duplicate(username):
        return "Username already exists"
    
    #check if email is valid, reg = "" if valid
    reg = errorMsg(email, password)
    if reg == "":
        #Create account with given info
        salt = urandom(10).encode('hex')
        
        query = ("INSERT INTO users (username,last_name,first_name,email,password,salt,level,phone_num) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (username, last, first, email, password, salt, account_level, phone_num))
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
        oldP = sha1(old+record[6]).hexdigest() #record[6] is the salt
        if record[5] == oldP:#record[5] is password
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

#-----------------------
# Change account level
#-----------------------
def change_level(key,new_level):
    db = connect(f)
    c = db.cursor()

    #change account level
    query = ("UPDATE users SET level=? WHERE primary_key=?")
    c.execute(query,(new_level,key,))
    db.commit()
    db.close()
    return "Account level changed."


#----------------------
# Turn off guest
#----------------------
def guest_off():
    db = connect(f)
    c = db.cursor()

    #get guest account
    query = ("SELECT * FROM users WHERE username='guest'")
    guest = c.execute(query)
    
    #change level to 5(disabled guest)
    for record in guest:
        key = record[0]
        return change_level(key,5)
    return "No guest account."

#---------------------
# Turn on guest
#---------------------
def guest_on():
    db = connect(f)
    c = db.cursor()

    #get guest account
    query = ("SELECT * FROM users WHERE username='guest'")
    guest = c.execute(query)
    
    #change level to 4(guest)
    for record in guest:
        key = record[0]
        return change_level(key,4)
    return "No guest account."


#-------------------------------
# Get name (last, first)
#-------------------------------
def get_name(username):
    db = connect(f)
    c = db.cursor()

    #get account with given username
    query = ("SELECT * FROM users WHERE username=?")
    account = c.execute(query,(username,)).fetchall()

    #return a string of last, first name
    last_first_name = ""
    for record in account:
        last_first_name = record[2] + ", " + record[3]
        return last_first_name
    return None


#-------------------------------
# Get name (last, first)
#-------------------------------
def get_email(username):
    db = connect(f)
    c = db.cursor()

    #get account with given username
    query = ("SELECT * FROM users WHERE username=?")
    account = c.execute(query,(username,)).fetchall()

    for record in account:
        return record[4]
    return None

#----------------------------
# get level
#----------------------------

def get_level(username):
    db = connect(f)
    c = db.cursor()

    #get account with given username
    query = ("SELECT * FROM users WHERE username=?")
    account = c.execute(query,(username,)).fetchall()

    for record in account:
        return record[7]
    return "username doesn't exist"


#----------------------
# Drop table(debug use)
#----------------------
def drop():
    db = connect(f)
    c = db.cursor()
    c.execute("DROP TABLE users")
    db.commit()
    db.close()
    return "Table users dropped"

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
def drop_users():
    db = connect(f)
    c = db.cursor()

    c.execute("DROP TABLE users")
    db.commit()
    db.close()
    return "users db dropped"


#-----------------------
# Testing area
#-----------------------

#drop_users()
#register("user1","last","first","email@stuy.edu","password123","password123",0,"1234567890")
#register("guest","","","test@test.com","password123","password123",4,"")
#register("teacher","Frizzle","Valerie","teacher@stuy.edu","password123",3,"9876543210")
#register("tech","Builder","Bob","tech@stuy.edu","password123",2,"1212121212")
#register("admin","Super","Man","admin@stuy.edu","password123",1,1234567890)
#print account_level("user1")
#print account_level("guest")

#guest_off()
#print account_level("guest")
#guest_on()
#print account_level("guest")

#print get_teacher_name("user1")
#print get_teacher_name("guest")

